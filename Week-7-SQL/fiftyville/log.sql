-- Get more details about the crime scene on Humphrey Street on July 28.
SELECT description FROM crime_scene_reports
WHERE month = 7 AND day = 28 AND street = 'Humphrey Street';

-- Understand the structure of the database and its relations.
.schema

-- Get interview details for July 28, 2024.
SELECT transcript, name FROM interviews
WHERE day = 28 AND month = 7 AND year = 2024;

-- Eugene saw the thief withdrawing money on Leggett Street, and Raymond overheard a phone call about leaving via the earliest flight.
--    Let's look for flight details and the origin airport.
SELECT * FROM airports;

-- Look at flights scheduled for July 29, 2024.
SELECT * FROM flights WHERE day = 29 AND year = 2024 AND month = 7;

-- Review passengers on flight 36 (Fiftyville to LaGuardia at 8:20 AM).
SELECT * FROM passengers WHERE flight_id = 36;

-- List passengers with matching passport numbers for flight 36.
SELECT name FROM people
WHERE passport_number IN (SELECT passport_number FROM passengers WHERE flight_id = 36);

-- Review phone calls on July 28, 2024, with duration under 5 minutes (Raymond seems suspicious).
SELECT * FROM phone_calls
WHERE day = 28 AND month = 7 AND year = 2024 AND duration <= 5;

-- Look at phone calls that were lengthy (500+ minutes) on July 28, 2024.
SELECT * FROM phone_calls
WHERE day = 28 AND month = 7 AND year = 2024 AND duration > 500;

-- Check bakery security logs for cars leaving after 10:20 AM on July 28, 2024.
SELECT license_plate FROM bakery_security_logs
WHERE hour = 10 AND minute >= 20 AND month = 7 AND day = 28 AND year = 2024 AND activity = 'exit';

-- Look at details of people associated with the license plates that left the bakery after 10:20 AM.
SELECT * FROM people
WHERE license_plate IN (SELECT license_plate FROM bakery_security_logs
                         WHERE hour = 10 AND minute >= 20 AND month = 7 AND day = 28 AND year = 2024 AND activity = 'exit');

-- Check for crimes committed at the ATM on Leggett Street on July 28, 2024.
SELECT description FROM crime_scene_reports
WHERE street = 'Leggett Street' AND year = 2024 AND day = 28 AND month = 7;

-- Look for ATM transactions at Leggett Street on July 28, 2024.
SELECT id FROM atm_transactions
WHERE transaction_type = 'withdraw' AND atm_location = 'Leggett Street' AND year = 2024 AND day = 28 AND month = 7;

-- Find the person IDs associated with the ATM withdrawal transactions on July 28, 2024.
SELECT person_id FROM bank_accounts
WHERE account_number IN (SELECT account_number FROM atm_transactions
                          WHERE transaction_type = 'withdraw' AND atm_location = 'Leggett Street'
                          AND year = 2024 AND day = 28 AND month = 7);

-- Retrieve the names of the people who made ATM withdrawals on July 28, 2024.
SELECT name FROM people
WHERE id IN (SELECT person_id FROM bank_accounts
             WHERE account_number IN (SELECT account_number FROM atm_transactions
                                      WHERE transaction_type = 'withdraw' AND atm_location = 'Leggett Street'
                                      AND year = 2024 AND day = 28 AND month = 7));

-- Check for phone calls on July 28, 2024, with durations under 60 seconds.
SELECT * FROM phone_calls
WHERE day = 28 AND month = 7 AND year = 2024 AND duration <= 60;

-- Get the names of callers with brief phone calls on July 28, 2024.
SELECT name FROM people
WHERE phone_number IN (SELECT caller FROM phone_calls
                        WHERE day = 28 AND month = 7 AND year = 2024 AND duration <= 60);

-- Get the names of phone call receivers on July 28, 2024, with brief calls.
SELECT name FROM people
WHERE phone_number IN (SELECT receiver FROM phone_calls
                        WHERE day = 28 AND month = 7 AND year = 2024 AND duration <= 60);

-- Check bakery security logs for cars exiting between 10:15 AM and 10:25 AM on July 28, 2024.
SELECT * FROM bakery_security_logs
WHERE year = 2024 AND month = 7 AND day = 28 AND hour = 10
AND minute > 15 AND minute < 25 AND activity = 'exit';

-- Check which people associated with license plates exited the bakery between 10:15 AM and 10:25 AM.
SELECT name FROM people
WHERE license_plate IN (SELECT license_plate FROM bakery_security_logs
                         WHERE year = 2024 AND month = 7 AND day = 28 AND hour = 10
                         AND minute > 15 AND minute < 25 AND activity = 'exit');

-- Conclusion: Based on security logs and phone call evidence, Bruce is the thief.
-- He called Robin, who is likely the accomplice.
-- The flight to LaGuardia at 8:20 AM on July 29 is part of the getaway plan.
