# Code review Max & Emily

- Meer comments
- Ik had heel veel try/except statements, dit was een beetje rommelig.
- Ook had ik een aantal except statements zonder specificatie van de error (enkel "except: (...)").
- Bij delete_cart had ik de boolean variabele is_added veranderd naar False, maar het is beter om delete() te gebruiken om een rommelige database te voorkomen.
- Er kwam nog een error als er een bestelling met een quantity van 0 werd geplaatst.
- Er was nog een beetje herhaling in de code.
- Na logout werd de gebruiker doorgestuurd naar index, doorsturen naar log in is misschien beter.
- Gebruikers kunnen  twee keer met hetzelfde emailadres registreren.
