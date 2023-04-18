# Keskustelupalstasovellus

### Tietokantasovellus harjoitustyö

Harjoitustyön aiheena on keskustelupalsta. Käyttäjän voivat luoda keskustelunavauksia sekä kommentoida toistensa avauksia ja kommentteja. Käyttäjät voivat navigoida helposti keskustelujen välillä, poistaa omia kommenttejaan ja avauksia, hakea keskusteluja otsikon perusteella ymv. Muita toiminnallisuuksia saatetaan lisätä kehityksen aikana.

### Sovelluksen testaaminen
Voit halutessasi kopioida sovelluksen omalle koneellesi. Näin käytät sitä:
1. Luo projektin app-hakemistoon `.env`-niminen tiedosto, jossa on muuttujat `DATABASE_URI` ja `SECRET_KEY`, ja aseta ensimmäiselle arvoksi paikallisen postgresql tietokannan osoite, ja jälimmäiselle jokin merkkijono.
2. Suorita seuraava komento: `psql < schema.sql`
3. Asenna riippuvuudet sovellukseen komennolla `poetry install`.
4. Suorita komento `poetry run invoke run`, ja mene osoitteeseen localhost:5000.

Huom. sovellukseen ei voi tavallinen käyttäjä luoda keskusteluaiheita käyttöliittymän kautta, luo jokin tulkin avulla, muutoin sovellus ei toimi kunnolla. Vaihtoehtoisesti voit luoda ylläpitäjäntunnukset, joilla niitä pystyy lisäämään: luo tulkin kautta admin-käyttäjä ```INSERT INTO users(username,passwordhash,admin) VALUES ('admin',[hash],true);```, missä [hash] on python-paketti werkzeug.security:n generate_password_hash:illa luotu merkkijono. 

Voit luoda hash-arvon esim. python tulkissa seuraavasti:
1. siiry poetryn tulkkiin: `poetry shell`
2. siirry python tulkkiin: `pyhton3`
3. Suorita: ```from werkzeug.security import generate_password_hash; generate_password_hash('[haluamasi merkkijono]')``` ja hash-arvo tulostuu näytölle.

### Sovelluksen tämänhetkinen tila
Sovellukseen voi luoda käyttäjän ja kirjautua sisään. Sisäänkirjautuneena voi luoda ja kommentoida keskusteluja, sekä poistaa omia viestejään. Sisäänkirjautumaton voi katsella sovelluksen keskusteluja ja kommentteja, muttei voi lisätä omia viestejään. Sovelluksen näkymien välillä voi navigoida sivuilla olevien linkkien avulla, sekä keskusteluja ja käyttäjiä voi hakea hakusanalla. Sovelluksen ylläpitäjät voivat poistaa käyttäjiä ja keskustelunaiheita. (Ylläpitäjää ei voi luoda käyttöliittymän kautta.)
