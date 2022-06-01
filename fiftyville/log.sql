-- I have two pieces of information----> Theft Date: July 28,2021 & Theft Place: Humphrey Street

SELECT description FROM crime_scene_reports;

-- Theft of CS50 duck at 10:15 Humphrey St bakery. 3 witness, all say bakery.
-- Let's check the interviews.
SELECT transcript FROM interviews
WHERE year = 2021 AND month = 7 AND day = 28;

-- Within ten minutes of the theft, thief got into car in the bakery parking lot and drove away. Security footage.
-- Earlier morning, he was withdrawing money from an ATM on Leggett St.
-- He called someone (and talked to under a minute) as he was leaving the bakery. He said buy the earliest flight tomorrow.

SELECT name FROM people
JOIN bakery_security_logs ON bakery_security_logs.license_plate = people.license_plate
WHERE year=2021 AND month=7 AND day=28 AND hour=10 AND minute >= 15 AND minute <= 25 AND activity="exit";
--Vanessa, Bruce, Barry, Luca, Sofia, Iman, Diana, Kelsey

SELECT name FROM people
JOIN bank_accounts ON bank_accounts.person_id = people.id
JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
WHERE atm_location LIKE "%Leggett%" AND transaction_type LIKE "%Withdraw%" AND year = 2021 AND month = 7 AND day = 28;
--Bruce, Diana, Brooke, Kenny, Iman, Luca, Taylor, Benista

--==> Common ones: Bruce, Diana, Luca, Iman.

SELECT id FROM airports
WHERE city ="Fiftyville";

SELECT name FROM people
JOIN passengers ON passengers.passport_number = people.passport_number
WHERE passengers.flight_id = (
SELECT id FROM flights
WHERE year = 2021 AND month = 7 AND day = 29 AND origin_airport_id = 8
ORDER BY hour, minute LIMIT 1);
--==> Commons: Bruce, Luca

SELECT name FROM people
JOIN phone_calls ON phone_calls.caller = people.phone_number
WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60;

--==> Common: Bruce (THIEF!)

SELECT city FROM airports
WHERE id = (SELECT destination_airport_id FROM flights
WHERE year = 2021 AND month = 7 AND day = 29 AND origin_airport_id = 8
ORDER BY hour, minute LIMIT 1);
--DESTINATION: NYC

SELECT phone_number FROM people WHERE name = "Bruce";
-- (367) 555-5533

SELECT name FROM people WHERE phone_number = (
    SELECT receiver FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND caller = "(367) 555-5533" AND duration < 60
);
--Robin

