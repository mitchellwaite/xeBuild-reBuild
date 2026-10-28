/*
 * timeutil.c: Win32 time conversions (SYSTEMTIME, FILETIME, DOS date/time)
 *
 * Derived from Wine's dlls/ntdll/time.c and dlls/kernel32/time.c, adapted
 * to cdecl functions that report errors through errno (EINVAL) and read the
 * clock with time().
 *
 * Copyright the Wine project authors.
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA
 */

#include <errno.h>
#include <stdlib.h>
#include <time.h>

#include "timeutil.h"

typedef short CSHORT;
typedef long long LONGLONG;
typedef unsigned long long ULONGLONG;

typedef union {
	struct {
		DWORD LowPart;
		DWORD HighPart;
	} u;
	LONGLONG QuadPart;
} LARGE_INTEGER;

typedef struct {
	WORD Year;
	WORD Month;
	WORD Day;
	WORD Hour;
	WORD Minute;
	WORD Second;
	WORD Milliseconds;
	WORD Weekday;
} TIME_FIELDS;

#define TICKSPERSEC        10000000
#define TICKSPERMSEC       10000
#define SECSPERDAY         86400
#define SECSPERHOUR        3600
#define SECSPERMIN         60
#define MINSPERHOUR        60
#define HOURSPERDAY        24
#define EPOCHWEEKDAY       1  /* Jan 1, 1601 was Monday */
#define DAYSPERWEEK        7
#define MONSPERYEAR        12
#define DAYSPERQUADRICENTENNIUM (365 * 400 + 97)
#define DAYSPERNORMALQUADRENNIUM (365 * 4 + 1)

/* 1601 to 1970 is 369 years plus 89 leap days */
#define SECS_1601_TO_1970  ((369 * 365 + 89) * (ULONGLONG)SECSPERDAY)
#define TICKS_1601_TO_1970 (SECS_1601_TO_1970 * TICKSPERSEC)

static const int MonthLengths[2][MONSPERYEAR] =
{
	{ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 },
	{ 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 }
};

static inline int IsLeapYear(int Year)
{
	return Year % 4 == 0 && (Year % 100 != 0 || Year % 400 == 0);
}

int RtlTimeFieldsToTime(TIME_FIELDS *tfTimeFields, LARGE_INTEGER *Time)
{
	int month, year, cleaps, day;

	/* native returns 0 (error) if the fields are not valid */
	if (tfTimeFields->Milliseconds > 999 ||
	    tfTimeFields->Second > 59 ||
	    tfTimeFields->Minute > 59 ||
	    tfTimeFields->Hour > 23 ||
	    tfTimeFields->Month < 1 || tfTimeFields->Month > 12 ||
	    tfTimeFields->Day < 1 ||
	    tfTimeFields->Day > MonthLengths
		[tfTimeFields->Month == 2 || IsLeapYear(tfTimeFields->Year)]
		[tfTimeFields->Month - 1] ||
	    tfTimeFields->Year < 1601)
		return 0;

	/* now calculate a day count from the date
	 * First start counting years from March. This way the leap days
	 * are added at the end of the year, not somewhere in the middle.
	 * Formula's become so much less complicate that way.
	 * To convert: add 12 to the month numbers of Jan and Feb, and
	 * take 1 from the year */
	if (tfTimeFields->Month < 3) {
		month = tfTimeFields->Month + 13;
		year = tfTimeFields->Year - 1;
	} else {
		month = tfTimeFields->Month + 1;
		year = tfTimeFields->Year;
	}
	cleaps = (3 * (year / 100) + 3) / 4;   /* nr of "century leap years"*/
	day =  (36525 * year) / 100 - cleaps + /* year * dayperyr, corrected */
	       (1959 * month) / 64 +           /* months * daypermonth */
	       tfTimeFields->Day -             /* day of the month */
	       584817;                         /* zero that on 1601-01-01 */
	/* done */

	Time->QuadPart = (((((LONGLONG)day * HOURSPERDAY +
		tfTimeFields->Hour) * MINSPERHOUR +
		tfTimeFields->Minute) * SECSPERMIN +
		tfTimeFields->Second) * 1000 +
		tfTimeFields->Milliseconds) * TICKSPERMSEC;

	return 1;
}

void RtlTimeToTimeFields(const LARGE_INTEGER *liTime, TIME_FIELDS *TimeFields)
{
	int SecondsInDay;
	long int cleaps, years, yearday, months;
	long int Days;
	ULONGLONG Time;

	/* Extract millisecond from time and convert time into seconds */
	TimeFields->Milliseconds =
		(CSHORT)((liTime->QuadPart % TICKSPERSEC) / TICKSPERMSEC);
	Time = liTime->QuadPart / TICKSPERSEC;

	/* The native version of RtlTimeToTimeFields does not take leap seconds
	 * into account */

	/* Split the time into days and seconds within the day */
	Days = Time / SECSPERDAY;
	SecondsInDay = Time % SECSPERDAY;

	/* compute time of day */
	TimeFields->Hour = (CSHORT)(SecondsInDay / SECSPERHOUR);
	SecondsInDay = SecondsInDay % SECSPERHOUR;
	TimeFields->Minute = (CSHORT)(SecondsInDay / SECSPERMIN);
	TimeFields->Second = (CSHORT)(SecondsInDay % SECSPERMIN);

	/* compute day of week */
	TimeFields->Weekday = (CSHORT)((EPOCHWEEKDAY + Days) % DAYSPERWEEK);

	/* compute year, month and day of month. */
	cleaps = (3 * ((4 * Days + 1227) / DAYSPERQUADRICENTENNIUM) + 3) / 4;
	Days += 28188 + cleaps;
	years = (20 * Days - 2442) / (5 * DAYSPERNORMALQUADRENNIUM);
	yearday = Days - (years * DAYSPERNORMALQUADRENNIUM) / 4;
	months = (64 * yearday) / 1959;
	/* the result is based on a year starting on March.
	 * To convert take 12 from Januari and Februari and
	 * increase the year by one. */
	if (months < 14) {
		TimeFields->Month = months - 1;
		TimeFields->Year = years + 1524;
	} else {
		TimeFields->Month = months - 13;
		TimeFields->Year = years + 1525;
	}
	/* calculation of day of month is based on the wonderful
	 * sequence of INT( n * 30.6): it reproduces the
	 * 31-30-31-30-31-31 month lengths exactly for small n's */
	TimeFields->Day = (CSHORT)(yearday - (1959 * months) / 64);
}

int FileTimeToSystemTime(const FILETIME *ft, SYSTEMTIME *syst)
{
	TIME_FIELDS tf;
	LARGE_INTEGER t;

	t.u.LowPart = ft->dwLowDateTime;
	t.u.HighPart = ft->dwHighDateTime;
	RtlTimeToTimeFields(&t, &tf);

	syst->wYear = tf.Year;
	syst->wMonth = tf.Month;
	syst->wDay = tf.Day;
	syst->wHour = tf.Hour;
	syst->wMinute = tf.Minute;
	syst->wSecond = tf.Second;
	syst->wMilliseconds = tf.Milliseconds;
	syst->wDayOfWeek = tf.Weekday;
	return 1;
}

int SystemTimeToFileTime(const SYSTEMTIME *syst, FILETIME *ft)
{
	TIME_FIELDS tf;
	LARGE_INTEGER t;

	tf.Year = syst->wYear;
	tf.Month = syst->wMonth;
	tf.Day = syst->wDay;
	tf.Hour = syst->wHour;
	tf.Minute = syst->wMinute;
	tf.Second = syst->wSecond;
	tf.Milliseconds = syst->wMilliseconds;

	if (!RtlTimeFieldsToTime(&tf, &t)) {
		errno = EINVAL;
		return 0;
	}
	ft->dwLowDateTime = t.u.LowPart;
	ft->dwHighDateTime = t.u.HighPart;
	return 1;
}

int FileTimeToDosDateTime(const FILETIME *ft, WORD *fatdate, WORD *fattime)
{
	LARGE_INTEGER li;
	ULONGLONG t;
	time_t unixtime;
	struct tm *tm;

	if (!fatdate || !fattime) {
		errno = EINVAL;
		return 0;
	}
	li.u.LowPart = ft->dwLowDateTime;
	li.u.HighPart = ft->dwHighDateTime;
	t = li.QuadPart / TICKSPERSEC - SECS_1601_TO_1970;
	if (li.QuadPart % TICKSPERSEC)
		t++;
	if (t & 1)
		t++;
	if (t > 0xffffffff) {
		errno = EINVAL;
		return 0;
	}
	unixtime = t;
	tm = gmtime(&unixtime);
	if (fattime)
		*fattime = (tm->tm_hour << 11) + (tm->tm_min << 5) + (tm->tm_sec / 2);
	if (fatdate)
		*fatdate = ((tm->tm_year - 80) << 9) + ((tm->tm_mon + 1) << 5)
			   + tm->tm_mday;
	return 1;
}

static void RtlSecondsSince1970ToTime(DWORD Seconds, LARGE_INTEGER *Time)
{
	Time->QuadPart = Seconds * (ULONGLONG)TICKSPERSEC + TICKS_1601_TO_1970;
}

int DosDateTimeToFileTime(WORD fatdate, WORD fattime, FILETIME *ft)
{
	struct tm newtm;
	struct tm *gtm;
	time_t time1, time2;

	newtm.tm_sec  = (fattime & 0x1f) * 2;
	newtm.tm_min  = (fattime >> 5) & 0x3f;
	newtm.tm_hour = (fattime >> 11);
	newtm.tm_mday = (fatdate & 0x1f);
	newtm.tm_mon  = ((fatdate >> 5) & 0x0f) - 1;
	newtm.tm_year = (fatdate >> 9) + 80;
	newtm.tm_isdst = -1;
	time1 = mktime(&newtm);
	gtm = gmtime(&time1);
	time2 = mktime(gtm);
	RtlSecondsSince1970ToTime(2 * time1 - time2, (LARGE_INTEGER *)ft);
	return 1;
}

void GetSystemTime(SYSTEMTIME *systime)
{
	FILETIME ft;
	LARGE_INTEGER t;

	t.QuadPart = (LONGLONG)time(NULL) * TICKSPERSEC + TICKS_1601_TO_1970;
	ft.dwLowDateTime = t.u.LowPart;
	ft.dwHighDateTime = t.u.HighPart;
	FileTimeToSystemTime(&ft, systime);
	/* time() has whole seconds only */
	srand(time(NULL));
	systime->wMilliseconds = (unsigned int)rand() % 999;
}
