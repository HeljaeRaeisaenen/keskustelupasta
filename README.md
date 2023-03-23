# Keskustelupalstasovellus

### Tietokantasovellus harjoitustyö

Harjoitustyön aiheena on keskustelupalsta. Käyttäjän voivat luoda keskustelunavauksia sekä kommentoida toistensa avauksia ja kommentteja. Käyttäjät voivat navigoida helposti keskustelujen välillä, poistaa omia kommenttejaan ja avauksia, kea keskusteluja otsikon perusteella ymv. Muita toiminnallisuuksia saatetaan lisätä kehityksen aikana.

### Sovelluksen testaaminen
Voit halutessasi kopioida sovelluksen omalle koneellesi. Sinun pitää luoda app-hakemistoon `.env`-niminen tiedosto, jossa on muuttujat `DATABASE_URI` ja `SECRET_KEY`, ja asettaa 1.:lle arvoksi paikallisen postgresql tietokannan osoite, ja jälimmäiselle jokin merkkijono. Avaa psql tulkki, kopioi siihen tiedoston schema.sql sisältö ja suorita. Kun olet asentanut riippuvuudet sovellukseen komennolla `poetry install`, sinun pitäisi voida suorittaa sovellus komennolla `poetry run invoke run`, jolloin voit päästä siihen osoitteesta localhost:5000.

Huom. sovellukseen ei voi vielä luoda keskusteluaiheita käyttöliittymän kautta, luo jokin tulkin avulla, muutoin sovellus ei toimi kunnolla.

### Sovelluksen tämänhetkinen tila
Sovellukseen voi luoda käyttäjän ja kirjautua sisään. Sisäänkirjautuneena voi luoda keskusteluja ja kommentoida keskusteluja. Sisäänkirjautumaton voi katsella sovelluksen keskusteluja ja kommentteja, muttei voi lisätä omia viestejään. Sovelluksen näkymien välillä voi navigoida sivuilla olevien linkkien avulla.


