CREATE STREAM TEMPERATURE_READINGS_TIMESTAMP_MT AS
SELECT TEMPERATURE, CONVERT_TZ(EVENTTIME_TS, 'UTC', 'America/Denver') AS EVENTTIME_MT
FROM TEMPERATURE_READINGS_TIMESTAMP;