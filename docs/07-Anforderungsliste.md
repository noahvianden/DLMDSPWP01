# DLMDSPWP01 – Master-Anforderungsliste und Ablauf bis zur Abgabe

Stand: 3. September 2026  
Status: Verbindliche Arbeitsgrundlage mit dokumentiertem tatsächlichem Arbeitsstand  
Kurs: DLMDSPWP01 – Programming with Python

## 1. Zweck und Arbeitsregel

Dieses Dokument ist die zentrale Anforderungs-, Ablauf- und Abnahmeliste für das gesamte Projekt. Eine Tätigkeit gilt erst dann als erledigt, wenn sowohl die Aufgabe ausgeführt als auch das genannte Ergebnis beziehungsweise der Nachweis geprüft wurde.

Statuskonvention:

- `[ ]` offen
- `[~]` in Bearbeitung
- `[x]` erledigt und geprüft
- `[!]` Entscheidung oder externe Bestätigung erforderlich

### Tatsächlicher Arbeitsstand (3. September 2026)

| Phase | Status | Nachweis |
|---|---|---|
| Phase 0 | erledigt | Entscheidungen, Rohdatenintegrität und Abgabeparameter sind dokumentiert. |
| Phase 1 | Baseline erledigt; einzelne Dokumentations-/Ausbaupunkte offen | Öffentliche Repository-Basis, Versionierung, Baseline-Test und Linter erfolgreich. |
| Phase 2 | erledigt gemäß Nutzerentscheidung | `docs/DATA_CONTRACT.md`; keine separate manuelle Datenprüfung und keine synthetischen Fixtures. |
| Phase 3 | erledigt | `docs/SOURCE_MATRIX.md` mit verifizierten Quellen und Fundstellen. |
| Phase 4 | erledigt | `docs/METHODOLOGY_AND_DESIGN.md` mit Regeln, Architektur und Teststrategie. |
| Phase 5 | erledigt | Implementierung in Commit `7e0afa9`; offizieller Lauf, SQLite, Bokeh und JSON-Zusammenfassung erfolgreich. |

Änderungen an Anforderungen werden in diesem Dokument nachvollziehbar festgehalten. Anforderungen dürfen nicht stillschweigend entfallen. Bei einem Konflikt gilt folgende Reihenfolge:

1. die zuletzt ausdrücklich bestätigten Entscheidungen des Studierenden,
2. die offizielle Aufgabenstellung und die aktuellen allgemeinen IU-Richtlinien,
3. die konsolidierten projektspezifischen Bewertungsrichtlinien,
4. dokumentierte eigene Designentscheidungen.

## 2. Verbindliche Projektentscheidungen

| ID | Entscheidung | Verbindliche Auslegung |
|---|---|---|
| E-01 | Aufgabenoption | Ausschließlich die offizielle Datensatzaufgabe `WrittenAssignment DLMDSPWP01`; keine Kombination mit einem eigenen Thema. |
| E-02 | Umfang | Höchstens 15 Inhaltsseiten von `Introduction` bis einschließlich `Conclusion`. Das Literaturverzeichnis wird nicht in diese 15 Seiten eingerechnet. Zitationen im Fließtext bleiben Bestandteil der Inhaltsseiten. |
| E-03 | Vorseiten | Deckblatt, Inhaltsverzeichnis sowie erforderliche Abbildungs-, Tabellen- und Abkürzungsverzeichnisse stehen vor der Introduction und werden nicht genutzt, um Inhalte aus dem 15-Seiten-Textteil auszulagern. |
| E-04 | Codebereitstellung | Der vollständige Anwendungscode liegt in einem für die prüfende Person zugänglichen Git-Repository, nicht im Anhang der Arbeit. |
| E-05 | Code im Dokument | Nur kurze, analytisch notwendige Codeausschnitte und die verlangten Git-Befehle dürfen in die Arbeit. Keine Codewiedergabe als Seitenfüller. |
| E-06 | Datensatz | Verwendet wird ausschließlich der bereitgestellte, unveränderte Datensatz. Die Originaldatei wird nicht inhaltlich bearbeitet. |
| E-07 | Daten im Repository | Die unveränderte Originaldatei `data/dataset.zip` wird auf ausdrückliche Entscheidung versioniert. Entpackte Original-CSV-Dateien, lokale SQLite-Dateien und generierte Ergebnisse bleiben ausgeschlossen; synthetische Fixtures werden nicht verwendet. |
| E-08 | Wissenschaftliche Quellen | Kursbuch, Vorlesungsfolien und Webinare werden nicht als zitierfähige Quellen verwendet. Fachliche Aussagen werden mit überprüften wissenschaftlichen Quellen oder – bei technischen Produkteigenschaften – mit offizieller Dokumentation belegt. |
| E-09 | Zitierstil | APA 7 mit den strengeren IU-Abweichungen, insbesondere Fundstellen auch bei auf konkrete Textstellen bezogenen Paraphrasen. |
| E-10 | Schreibstil | Formal, objektiv und analytisch; bevorzugt Passiv, erforderlichenfalls `the author`, kein Tagebuchstil und keine unbegründeten Wertungen. |
| E-11 | Nicht erforderliche Teile | Kein Abstract, keine eigenständige umfangreiche Literature Review, keine Acknowledgements und kein separater Abschnitt `Future Work`, sofern keine spätere verbindliche Vorgabe dies verlangt. |
| E-12 | Reproduzierbarkeit | Eine fachkundige prüfende Person kann das Repository frisch klonen, Abhängigkeiten installieren, das versionierte Archiv lokal entpacken, Programm und Tests ausführen und die berichteten Ergebnisse erzeugen. |

### Verbindliches Quellenregister

| Source-ID | Projektquelle | Verwendungszweck |
|---|---|---|
| S-01 | `dataset.zip` | Unveränderliche Eingabedaten mit `train.csv`, `ideal.csv` und `test.csv` |
| S-02 | `General Citation Guidelines.pdf` | APA 7 mit IU-Abweichungen, Quellenqualität, Textzitate, Abbildungen/Tabellen und Literaturverzeichnis |
| S-03 | `Guidelines Written Assignment.pdf` | Ziel, Aufbau, Bestandteile, Umfang, Einreichung und Bewertungsgewichtung |
| S-04 | `Guideline for Avoiding Plagiarism.pdf` | Plagiatsarten, Turnitin, Eigenständigkeit und Präventionskontrollen |
| S-05 | `projektquelle_bewertungsrichtlinien.txt` | Konsolidierte projektspezifische Schreib-, Argumentations-, Struktur- und Codevorgaben |
| S-06 | `Task_WrittenAssignment_DLMDSPWP01.pdf` | Verbindliche technische Aufgabe einschließlich Datenbank-, OOP-, Test-, Visualisierungs- und Git-Anforderungen |

Die Projektquellen dienen als Prüfungs- und Arbeitsvorgaben. Soweit sie Kursmaterial darstellen, werden sie nicht als wissenschaftliche Fachliteratur zur Begründung theoretischer Behauptungen missbraucht.

## 3. Zielbild und Definition of Done

Die Abgabe ist erst fertig, wenn alle folgenden Bedingungen gleichzeitig erfüllt sind:

- [ ] Das Programm erfüllt jeden technischen Punkt der offiziellen Aufgabe.
- [ ] Jede der vier Trainingsreihen wurde anhand der minimalen Summe quadrierter y-Abweichungen einer Ideal-Funktion zugeordnet.
- [ ] Jeder der 100 Testpunkte wurde geprüft und entweder eindeutig zugeordnet oder nachvollziehbar als nicht zuordenbar behandelt.
- [ ] Das vorgeschriebene `sqrt(2)`-Kriterium wurde mathematisch korrekt, deterministisch und getestet umgesetzt.
- [ ] SQLite enthält die verlangten Tabellenstrukturen und die korrekten Zuordnungsergebnisse.
- [ ] Pandas, SQLAlchemy und Bokeh werden fachlich sinnvoll eingesetzt.
- [ ] Die Architektur ist sinnvoll objektorientiert und enthält eine fachlich begründete Vererbungsbeziehung.
- [ ] Standard- und eigene Exceptions werden sinnvoll ausgelöst, behandelt und getestet.
- [ ] Der gesamte selbst geschriebene Code enthält angemessene Modul-, Klassen-, Methoden- und Funktions-Docstrings.
- [ ] Unit-, Integrations- und End-to-End-Tests laufen vollständig erfolgreich.
- [ ] Die Visualisierungen decken Trainingsdaten, ausgewählte Ideal-Funktionen, Testdaten, Zuordnungen und Abweichungen logisch ab.
- [ ] Das Repository ist sauber, reproduzierbar, dokumentiert, versioniert und für die Bewertung erreichbar.
- [ ] Die Arbeit erklärt lückenlos, was getan wurde, warum es getan wurde, wie es umgesetzt wurde und was die Ergebnisse bedeuten.
- [ ] Methodik und Design stehen in der Argumentation vor der Implementierung.
- [ ] Jede fachliche Fremdaussage ist passend belegt; jede Quelle ist verifiziert; Textzitate und Literaturverzeichnis stimmen in beide Richtungen überein.
- [ ] Jede Abbildung und Tabelle besitzt Nummer, aussagekräftigen Titel, Quellenzeile, Textverweis und Interpretation.
- [ ] Der Textteil überschreitet 15 Seiten nicht.
- [ ] Alle formalen IU-Vorgaben, die elektronische Eigenständigkeitserklärung und der Turnitin-Upload sind abschließend geprüft.
- [ ] Die hochgeladene Datei und der im Text genannte Repository-Stand entsprechen exakt der final freigegebenen Version.

## 4. Chronologischer Masterablauf

### Phase 0 – Anforderungen einfrieren und Projekt kontrolliert starten

- [x] ~~**A-001 – Quellenregister anlegen.** Alle sechs Projektquellen mit Titel, Datum/Version, Zweck und Verbindlichkeit erfassen.~~ Nachweis: Abschnitt 2, „Verbindliches Quellenregister“.
- [x] ~~**A-002 – Nutzerentscheidungen protokollieren.** Maximal 15 Inhaltsseiten ohne Literaturverzeichnis und Repository statt Codeanhang als bindende Entscheidungen festhalten.~~ Nachweis: E-02 und E-04.
- [x] ~~**A-003 – Aufgabenoption festschreiben.** Offizielle Datensatzaufgabe als einzige Option dokumentieren.~~ Nachweis: E-01.
- [x] ~~**A-004 – Originaldaten sichern.** `dataset.zip` schreibgeschützt beziehungsweise unverändert als Rohquelle behandeln.~~ Nachweis: SHA-256 `829d38351e8878982d34c170f16a6351aa30bed8ff43e8a68b4ec026ebc45ed4`.
- [x] ~~**A-005 – Archivintegrität prüfen.** ZIP-Test muss für `train.csv`, `ideal.csv` und `test.csv` fehlerfrei sein.~~ Nachweis: erfolgreicher `unzip -t`-Test dokumentiert.
- [x] ~~**A-006 – Aktuelle Einreichungsparameter notieren.** Abgabedatum, Zeitzone, zulässiges Dateiformat, Dateinamensregel, Sprache des Studiengangs und Turnitin-Kurs aus myCampus erfassen.~~ Nachweis: 06.09.2026, UTC+01:00, PDF, `NachnameName_MatrikelNummer_Kursname.pdf`, Englisch, Turnitin-Kurs beliebig.
- [x] ~~**A-007 – Formatvorlage bestätigen.** Aktuelle IU-Richtlinie zur Strukturierung und Formatierung akademischer Arbeiten beziehungsweise das gültige Template prüfen.~~ Auf ausdrückliche Nutzerentscheidung gestrichen; die verbliebenen formalen Pflichtprüfungen bleiben in den Endphasen erhalten.
- [x] ~~**A-008 – Abgabesprache bestätigen.** Sprache gemäß Kurs-/Prüfungsvorgabe verbindlich festlegen; bei englischer Abgabe englische Terminologie und APA-Beispiele konsistent verwenden.~~ Nachweis: verbindliche Entscheidung „Englisch“.
- [x] ~~**A-009 – Arbeitstitel festlegen.** Arbeitsfassung: *Object-Oriented Selection and Mapping of Ideal Functions in Python: A Least-Squares and SQLite-Based Approach*.~~ Nachweis: Titel deckt Methode, Anwendung und Scope ab.
- [x] ~~**A-010 – Forschungsfrage festlegen.** Arbeitsfassung: *How can an object-oriented Python application reproducibly select the four best-fitting ideal functions using a least-squares criterion, assign eligible test points under the prescribed deviation threshold, and persist and visualize the resulting mappings?*~~ Nachweis: verbindliche Forschungsfrage.
- [x] ~~**A-011 – Ziel definieren.** Ziel ist nicht nur ein lauffähiges Programm, sondern eine begründete, reproduzierbare und kritisch bewertete Lösung der offiziellen Aufgabe.~~ Nachweis: Zielbild in Abschnitt 3.
- [x] ~~**A-012 – Scope festlegen.** Im Scope: Datenvalidierung, Ideal-Funktionsauswahl, Punktzuordnung, SQLite, Visualisierung, Tests, Fehlerbehandlung und Git-Workflow.~~ Nachweis: Scopeentscheidung in Abschnitt 2.
- [x] ~~**A-013 – Out-of-Scope festlegen.** Nicht im Scope: Schätzung neuer Funktionsparameter, Prognose außerhalb des x-Bereichs, Vergleich konkurrierender ML-Modelle, Web-GUI, produktiver Datenbankserver und beliebige Erweiterungen ohne Beitrag zur Forschungsfrage.~~ Nachweis: Scopeentscheidung in Abschnitt 2.
- [x] ~~**A-014 – Begriffliche Präzision sichern.** Die Lösung wählt aus vorgegebenen Funktionen; sie trainiert kein neues Regressionsmodell. Der Begriff `least-squares criterion` ist gegenüber pauschalen Aussagen über lineare Regression zu bevorzugen.~~ Nachweis: E-01 und `docs/SOURCE_MATRIX.md`.
- [x] ~~**A-015 – Seitenbudget reservieren.** Das in Abschnitt 6 definierte Budget verbindlich als Obergrenze pro Abschnitt übernehmen.~~ Nachweis: 15-Seiten-Grenze in E-02 und Abschnitt 6.
- [x] ~~**A-016 – Bewertungsgewichtung in die Planung übernehmen.** Besondere Prüftiefe für Reasoning (40 %), Struktur (15 %) und Conclusion (15 %) vorsehen.~~ Nachweis: Planungsprioritäten dokumentiert.
- [x] ~~**A-017 – Offene Konflikte schließen.** In allen Arbeitsunterlagen alte Angaben von 15–20 Seiten und Code im Anhang als überholt kennzeichnen.~~ Nachweis: E-02, E-04 und E-05 ersetzen die abweichenden Vorgaben.
- [x] ~~**A-018 – Änderungsregel festlegen.** Neue Anforderungen werden mit Datum, Quelle, Auswirkung und Entscheidung in diesem Dokument ergänzt.~~ Nachweis: Abschnitt 10.

**Abnahme Phase 0: erledigt.** Forschungsfrage, Scope, Titel, Umfang, Abgabesprache und Einreichungsparameter sind eindeutig. A-007 ist als bewusste Auslassung dokumentiert.

### Phase 1 – Repository, Entwicklungsumgebung und Nachweisführung einrichten

- [x] ~~**A-019 – Repository anlegen.** Git-Repository mit nachvollziehbarem Namen und eindeutigem Bezug zu DLMDSPWP01 erstellen.~~ Nachweis: `https://github.com/noahvianden/DLMDSPWP01`.
- [x] ~~**A-020 – Sichtbarkeit festlegen.** Öffentlich oder privat so konfigurieren, dass die prüfende Person dauerhaft Zugriff erhält; Datenfreigaberegeln berücksichtigen.~~ Nachweis: Repository ist öffentlich und Zugriff wurde geprüft.
- [x] ~~**A-021 – Branch-Struktur anlegen.** Mindestens `main`, `develop` und für Änderungen `feature/<name>` verwenden.~~ Nachweis: Branches `main` und `develop` vorhanden; neue abgegrenzte Änderungen folgen `feature/<name>`.
- [~] **A-022 – Initialen Commit erstellen.** Strukturierte Projektbasis mit README, `.gitignore` und Abhängigkeitsdatei ist versioniert (u. a. Commit `505b573`). Die Lizenzentscheidung bleibt ausdrücklich offen.
- [x] ~~**A-023 – Python-Version festlegen.** Unterstützte Python-Version dokumentieren und lokal sowie in automatisierten Prüfungen identisch verwenden.~~ Nachweis: `pyproject.toml` mit `>=3.11,<3.14`.
- [x] ~~**A-024 – Abhängigkeiten definieren.** Pandas, SQLAlchemy, Bokeh, pytest und notwendige Hilfspakete mit reproduzierbaren Versionen festhalten.~~ Nachweis: `pyproject.toml`.
- [x] ~~**A-025 – Virtuelle Umgebung dokumentieren.** Installations- und Aktivierungsschritte betriebssystemneutral beziehungsweise für die Zielumgebung eindeutig beschreiben.~~ Nachweis: README-Entwicklungsbefehle mit `python -m venv .venv`.
- [~] **A-026 – Projektlayout anlegen.** Die Paket-, Test-, Daten-, Output- und Dokumentationsstruktur ist angelegt. Die erst in Phase 5 zu implementierenden Fachmodule bleiben offen:

  ```text
  repository/
  ├── README.md
  ├── pyproject.toml
  ├── .gitignore
  ├── src/ideal_function_assignment/
  │   ├── __init__.py
  │   ├── config.py
  │   ├── exceptions.py
  │   ├── loaders.py
  │   ├── database.py
  │   ├── selection.py
  │   ├── mapping.py
  │   ├── visualization.py
  │   └── main.py
  ├── tests/
  │   ├── unit/
  │   ├── integration/
  │   └── fixtures/
  ├── data/        # versioniertes Archiv, entpackte CSV ignoriert
  └── output/      # reproduzierbare Laufzeitergebnisse
  ```

- [x] ~~**A-027 – Laufzeitdaten und Artefakte ausschließen.** Entpackte Original-CSV-Dateien, lokale SQLite-Datei, Caches, Umgebungen und sensible Dateien in `.gitignore` aufnehmen.~~ Nachweis: `.gitignore`; bewusste Ausnahme ist das unveränderte, versionierte `data/dataset.zip`.
- [x] ~~**A-028 – Synthetische Fixtures anlegen.** Kleine, selbst erstellte CSV-Dateien für Unit- und Integrationstests bereitstellen; keine Teilkopien des individuellen Datensatzes veröffentlichen.~~ Auf ausdrückliche Nutzerentscheidung nicht erforderlich; angelegte Fixtures wurden entfernt.
- [~] **A-029 – Qualitätswerkzeuge festlegen.** `pytest` und `ruff` sind in `pyproject.toml` konfiguriert und erfolgreich ausgeführt; die vollständigen Qualitätsbefehle müssen noch im README ergänzt werden.
- [x] ~~**A-030 – Arbeitsprotokoll etablieren.** Entscheidungen, Annahmen, Testergebnisse, Abbildungen und Quellen unmittelbar bei ihrer Entstehung dokumentieren.~~ Nachweis: `docs/WORKLOG.md`.
- [x] ~~**A-031 – Commit-Regeln festlegen.** Kleine, fachlich geschlossene Commits mit aussagekräftigen Nachrichten; keine Sammelcommits kurz vor Abgabe.~~ Nachweis: `docs/WORKLOG.md`, „Commit rules“.
- [~] **A-032 – Reproduzierbarkeitsbefehl planen.** Der zentrale CLI-Aufruf ist als Ziel für Phase 5 / A-099 festgelegt; Implementierung und README-Befehl sind noch offen.
- [x] ~~**A-033 – Baseline-Prüfung ausführen.** Installation, Import der leeren Paketstruktur, Linter und initialer Testlauf müssen funktionieren.~~ Nachweis: frische `.venv`, `pip install -e '.[dev]'`, pytest: 1 passed, Ruff: all checks passed, Paketimport: `0.1.0`.

**Zwischenstand Phase 1:** Die technische Baseline ist erfolgreich validiert. Offen bleiben nur die Lizenzentscheidung, der spätere Modul-/CLI-Ausbau und die vollständige README-Qualitätsdokumentation (A-022, A-026, A-029, A-032).

### Phase 2 – Datensatz untersuchen und Datenvertrag definieren

- [ ] **A-034 – Dateien kontrolliert entpacken.** Nur in das ignorierte lokale Datenverzeichnis; Dateinamen unverändert beibehalten.
- [x] ~~**A-035 – CSV-Schema prüfen.** `train.csv`: `x,y1,y2,y3,y4`; `ideal.csv`: `x,y1…y50`; `test.csv`: `x,y`.~~ Auf ausdrückliche Nutzerentscheidung kein separater Datencheck; das Schema wird als bereitgestellter Datenvertrag übernommen.
- [x] ~~**A-036 – Dimensionen prüfen.** Training: 400 × 5; Ideal-Funktionen: 400 × 51; Test: 100 × 2.~~ Auf ausdrückliche Nutzerentscheidung kein separater Datencheck.
- [x] ~~**A-037 – Datentypen prüfen.** Sämtliche x- und y-Werte müssen numerisch und endlich sein; keine stillschweigende Konvertierung fehlerhafter Werte.~~ Auf ausdrückliche Nutzerentscheidung kein separater Datencheck.
- [x] ~~**A-038 – Fehlwerte prüfen.** Für den gelieferten Datensatz werden keine fehlenden Werte erwartet; fehlende Werte müssen eine definierte Exception auslösen.~~ Auf ausdrückliche Nutzerentscheidung kein separater Datencheck.
- [x] ~~**A-039 – x-Bereich prüfen.** Training und Ideal-Funktionen: −20,0 bis 19,9 in Schritten von 0,1.~~ Auf ausdrückliche Nutzerentscheidung kein separater Datencheck.
- [x] ~~**A-040 – x-Ausrichtung prüfen.** Trainings- und Ideal-Daten müssen dieselben 400 x-Werte in eindeutiger Zuordnung besitzen.~~ Auf ausdrückliche Nutzerentscheidung kein separater Datencheck.
- [x] ~~**A-041 – Test-x-Abdeckung prüfen.** Jeder Test-x-Wert muss in den Ideal-Funktionen vorhanden sein; für unbekannte x-Werte ist ein definierter Fehler- beziehungsweise Nichtzuordnungsweg festzulegen.~~ Auf ausdrückliche Nutzerentscheidung kein separater Datencheck; die Anwendung behandelt später fehlende Eingabedateien sinnvoll.
- [x] ~~**A-042 – Duplikatregel festlegen.** Training und Ideal-Funktionen dürfen keine doppelten x-Werte enthalten. Testdaten dürfen wiederholte x-Werte enthalten.~~ Auf ausdrückliche Nutzerentscheidung kein separater Datencheck; technische Identität der Ergebniszeilen ist dennoch festgelegt.
- [x] ~~**A-043 – Datenbankfolge ableiten.** `x` darf deshalb in der Ergebnistabelle nicht als eindeutiger Primärschlüssel verwendet werden; die SQLite-interne Row-ID oder eine nicht sichtbare technische Identität genügt, während die vier verlangten Fachspalten erhalten bleiben.~~ Nachweis: `docs/DATA_CONTRACT.md`, „Operational rules“.
- [x] ~~**A-044 – Sortierung festlegen.** Berechnungen werden über x-Schlüssel ausgerichtet und nicht lediglich über zufällige Zeilenpositionen; Ausgaben erhalten eine dokumentierte stabile Reihenfolge.~~ Nachweis: `docs/DATA_CONTRACT.md`.
- [x] ~~**A-045 – Fließkommaregel festlegen.** x-Schlüssel aus den gelieferten Tabellen werden konsistent normalisiert/zusammengeführt; y-Vergleiche verwenden volle Rechengenauigkeit, Rundung nur für Darstellung.~~ Nachweis: `docs/DATA_CONTRACT.md`.
- [x] ~~**A-046 – Validierungsbericht erzeugen.** Schema, Zeilenzahlen, Wertebereiche, Fehlwerte, Duplikate und x-Kompatibilität maschinenlesbar oder im Log ausgeben.~~ Auf ausdrückliche Nutzerentscheidung nicht erforderlich; der bereitgestellte Datensatz wird als korrekt behandelt.
- [x] ~~**A-047 – Datenbeschreibung für die Arbeit vorbereiten.** Nur relevante Eigenschaften berichten und interpretieren; keine komplette Rohdatentabelle abdrucken.~~ Nachweis: `docs/DATA_CONTRACT.md` begrenzt die spätere Datenbeschreibung auf relevante Eigenschaften.

**Abnahme Phase 2: erledigt gemäß Nutzerentscheidung.** Der Datenvertrag definiert Eingaben und operative Regeln; eine gesonderte manuelle Datenprüfung und ein Validierungsbericht sind bewusst ausgeschlossen. A-034 bleibt für den späteren Programmlauf offen.

### Phase 3 – Wissenschaftliche Quellenbasis und mathematische Grundlage erarbeiten

- [x] ~~**A-048 – Suchbegriffe definieren.** Least squares/SSE, Residuen und Abweichungsmaße, objektorientiertes Design, Datenpersistenz, Softwaretests und Datenvisualisierung.~~ Nachweis: `docs/SOURCE_MATRIX.md`, „Search record“.
- [x] ~~**A-049 – Quellenhierarchie anwenden.** Peer-reviewed Original- oder Standardliteratur für mathematische und methodische Aussagen; offizielle Pandas-, SQLAlchemy-, Bokeh-, Python- und pytest-Dokumentation nur für konkrete technische Eigenschaften.~~ Nachweis: `docs/SOURCE_MATRIX.md`, „Source hierarchy“.
- [x] ~~**A-050 – Kursmaterial ausschließen.** Kursbuch, Folien und Webinare nicht in das Literaturverzeichnis aufnehmen.~~ Nachweis: `docs/SOURCE_MATRIX.md`, „Purpose and use rule“.
- [x] ~~**A-051 – Jede Quelle verifizieren.** Autor, Jahr, Titel, Publikationsort/Journal, DOI/URL, tatsächliche Existenz und inhaltliche Passung prüfen.~~ Nachweis: die verifizierten Referenzdatensätze MATH-01 bis TECH-04 in `docs/SOURCE_MATRIX.md`.
- [x] ~~**A-052 – Fundstellen erfassen.** Für jede übernommene Aussage exakte Seite, Seitenbereich, Abschnitt oder – nur wenn keine Seiten vorhanden sind – geeignete alternative Fundstelle notieren.~~ Nachweis: Seitenbereich für Hastie et al.; benannte Abschnitte für NIST und die offiziellen Dokumentationen.
- [x] ~~**A-053 – Quellenmatrix führen.** Spalten: Behauptung, Quelle, Fundstelle, Qualität, vorgesehener Abschnitt, Paraphrase/Direktzitat, Verifikationsstatus.~~ Nachweis: `docs/SOURCE_MATRIX.md`, „Claim matrix“.
- [x] ~~**A-054 – Mathematische Quelle auswählen.** Eine geeignete Quelle muss die Bedeutung der Summe quadrierter Abweichungen stützen; die aufgabenspezifische Anwendung wird als eigene Methodik erklärt.~~ Nachweis: MATH-01 (NIST/SEMATECH), Abschnitt 4.1.4.1.
- [x] ~~**A-055 – Technische Quellen sparsam einsetzen.** Eigene Implementierungsschritte wie das Einlesen in einen DataFrame benötigen keine Quelle. Produktbehauptungen werden nur belegt, wenn sie argumentativ relevant sind.~~ Nachweis: bedingte TECH-01 bis TECH-04.
- [x] ~~**A-056 – Sekundärzitate vermeiden.** Originalquelle beschaffen; nur bei tatsächlicher Nichtverfügbarkeit `as cited in` nach IU-Regel verwenden.~~ Nachweis: ausdrückliche Regel in `docs/SOURCE_MATRIX.md`.
- [x] ~~**A-057 – Literaturverwaltung vorbereiten.** Einheitlichen APA-7/IU-Stil, Anhänge für Seitennummern und vollständige Metadaten konfigurieren.~~ Nachweis: Quellenschlüssel, APA-Referenzdaten und „Final citation controls“ in `docs/SOURCE_MATRIX.md`.
- [x] ~~**A-058 – Quellenpaket einfrieren.** Vor dem Volltextentwurf ausreichend belastbare Quellen für alle theoretischen Aussagen verfügbar haben; keine nachträglich erfundenen Belege.~~ Nachweis: Quellenpaket ist für die derzeit geplanten Aussagen freigegeben; neue Theoriebehauptungen benötigen vor Nutzung einen neuen verifizierten Quelleneintrag.

**Abnahme Phase 3: erledigt.** Die derzeit geplanten theoretischen Aussagen besitzen überprüfte Quellen und Fundstellen; technische Dokumentationen bleiben konditional und werden nicht dekorativ zitiert.

### Phase 4 – Methodik und Systemdesign vor der Implementierung festlegen

- [x] ~~**A-059 – Notation definieren.** Eindeutige Notation für x, Trainingsreihen, Ideal-Funktionen und Testpunkte festlegen.~~ Nachweis: docs/METHODOLOGY_AND_DESIGN.md, Abschnitt 1.
- [x] ~~**A-060 – Auswahlkriterium definieren.** Die SSE-Formel für jede Trainings-/Ideal-Funktionskombination festlegen.~~ Nachweis: Abschnitt 2.1.
- [x] ~~**A-061 – Auswahlregel definieren.** Jede Trainingsreihe unabhängig mit minimaler SSE auswählen; exakte Gleichstände deterministisch über die kleinste Funktionsnummer auflösen.~~ Nachweis: Abschnitt 2.1.
- [x] ~~**A-062 – Maximalabweichung definieren.** Für jedes gewählte Paar die größte absolute Trainingsabweichung berechnen.~~ Nachweis: Abschnitt 2.1.
- [x] ~~**A-063 – Testabweichung definieren.** Die absolute y-Abweichung eines Testpunkts zur ausgewählten Ideal-Funktion festlegen.~~ Nachweis: Abschnitt 2.2.
- [x] ~~**A-064 – Zulässigkeitsregel definieren.** Ein Kandidat ist bei Abweichung kleiner oder gleich sqrt(2) mal Maximalabweichung zulässig; Gleichheit ist zulässig.~~ Nachweis: Abschnitt 2.2.
- [x] ~~**A-065 – Mehrfachtrefferregel definieren.** Mehrere zulässige Kandidaten über die kleinste absolute Abweichung und anschließend die kleinste Funktionsnummer auflösen.~~ Nachweis: Abschnitt 2.2.
- [x] ~~**A-066 – Nichttrefferregel definieren.** Nicht zuordenbare Punkte zählen und als unassigned erhalten, aber nicht in die vierfachspaltige Ergebnistabelle schreiben.~~ Nachweis: Abschnitt 2.2.
- [x] ~~**A-067 – Vollständigkeitsinvariante definieren.** Zuordnungen plus Nichtzuordnungen müssen genau der Zahl eingelesener Testzeilen entsprechen.~~ Nachweis: Abschnitt 2.2.
- [x] ~~**A-068 – Delta-Semantik definieren.** delta_y ist die nichtnegative absolute Abweichung; ein signierter Residuenwert ist höchstens intern ergänzend.~~ Nachweis: Abschnitt 1 und 2.2.
- [x] ~~**A-069 – x-Matching definieren.** Nur identische gelieferte x-Werte vergleichen; keine Interpolation, Extrapolation oder Nächster-Nachbar-Ersetzung.~~ Nachweis: Abschnitt 2.2.
- [x] ~~**A-070 – Zeilenweises Mapping definieren.** Testdaten über einen Iterator zeilenweise laden und unmittelbar auswerten.~~ Nachweis: Abschnitt 2.3 und 4.
- [x] ~~**A-071 – Datenbankmodell festlegen.** Die drei Pflichttabellen mit den verlangten Fachspalten festlegen.~~ Nachweis: Abschnitt 3.
- [x] ~~**A-072 – Zusatztabelle begründen.** selection_summary mit Auswahl-, SSE- und Schwellenwerten als Reproduzierbarkeitsnachweis festlegen.~~ Nachweis: Abschnitt 3.
- [x] ~~**A-073 – Datenbanktypen und Constraints festlegen.** Numerische Spalten, eindeutiges x in Referenztabellen, SQLite-rowid für Ergebniszeilen und Transaktionsregel festlegen.~~ Nachweis: Abschnitt 3.
- [x] ~~**A-074 – OOP-Verantwortlichkeiten festlegen.** Laden, Auswahl, Mapping, Persistenz, Visualisierung und Orchestrierung trennen.~~ Nachweis: Abschnitt 4.
- [x] ~~**A-075 – Sinnvolle Vererbung festlegen.** BaseCSVLoader mit drei fachlich begründeten Spezialisierungen festlegen.~~ Nachweis: Abschnitt 4.1.
- [x] ~~**A-076 – Exception-Hierarchie festlegen.** Gemeinsame Projektbasis und fachliche Unterklassen für Daten, Auswahl, Mapping, Persistenz und Visualisierung definieren.~~ Nachweis: Abschnitt 4.2.
- [x] ~~**A-077 – Standard-Exceptions festlegen.** Datei-, Parser-, Typ-, Schlüssel- und SQLAlchemy-Fehler an Komponentengrenzen behandeln und fachlich übersetzen.~~ Nachweis: Abschnitt 4.2.
- [x] ~~**A-078 – Transaktionsverhalten festlegen.** Erfolgreicher vollständiger Lauf oder Rollback; keine unvollständige Datenbank als Erfolg melden.~~ Nachweis: Abschnitt 3 und 4.2.
- [x] ~~**A-079 – Visualisierungskonzept festlegen.** Vier vergleichbare Panels, testpunktbezogene Hover-Daten, unzugeordnete Punkte und Abweichungsdarstellung festlegen.~~ Nachweis: Abschnitt 5.
- [x] ~~**A-080 – Teststrategie vor Code festlegen.** Unit-, Integrations-, End-to-End- und Reproduzierbarkeitstests mit In-Memory-Testdaten statt CSV-Fixtures definieren.~~ Nachweis: Abschnitt 6.
- [x] ~~**A-081 – Architekturdiagramm entwerfen.** Datenfluss und Komponenten als Mermaid-Diagramm dokumentieren.~~ Nachweis: Abschnitt 4.
- [x] ~~**A-082 – Designentscheidungen begründen.** Alternativen, Vorteile, Konsequenzen und Aufgabenbezug dokumentieren.~~ Nachweis: Abschnitt 7.

**Abnahme Phase 4: erledigt.** Formeln, Randfallregeln, Datenbank, Klassenverantwortlichkeiten, Vererbung, Exceptions, Visualisierung und Teststrategie sind vor dem Produktivcode verbindlich dokumentiert.

### Phase 5 – Anwendung in festgelegter Reihenfolge implementieren

- [x] ~~**A-083 – Konfiguration implementieren.** Pfade, Datenbankziel, Ausgabeverzeichnis und Logging zentral, validierbar und ohne fest codierte persönliche Pfade verwalten.~~ Nachweis: `src/ideal_function_assignment/config.py` (`AppConfig`) and CLI configuration.
- [x] ~~**A-084 – Exception-Klassen implementieren.** Klare Fehlermeldungen mit Ursache und betroffener Datei/Funktion; Exception-Chaining verwenden.~~ Nachweis: `src/ideal_function_assignment/exceptions.py` plus chained component-boundary errors.
- [x] ~~**A-085 – Basisklasse für Loader implementieren.** Gemeinsame Dateiexistenz-, Header-, Datentyp-, Fehlwert- und Duplikatprüfungen.~~ Nachweis: `BaseCSVLoader` in `src/ideal_function_assignment/loaders.py`.
- [x] ~~**A-086 – Spezialisierte Loader implementieren.** Trainings-, Ideal- und Testregeln getrennt ergänzen; Liskov-konformes Verhalten sicherstellen.~~ Nachweis: `TrainingDataLoader`, `IdealFunctionLoader`, and line-by-line `TestDataLoader`.
- [x] ~~**A-087 – Datenbankkomponente implementieren.** SQLAlchemy-Engine, Metadaten/Tabellen, Transaktionen und deterministische Neuanlage beziehungsweise Ersetzung.~~ Nachweis: `DatabaseRepository` / `DatabaseRun` with SQLAlchemy Core and atomic replacement.
- [x] ~~**A-088 – Trainingstabelle schreiben.** Exakt 400 Zeilen und fünf Fachspalten nach erfolgreicher Validierung.~~ Nachweis: official-archive run: 400 rows and five `training_data` columns.
- [x] ~~**A-089 – Ideal-Tabelle schreiben.** Exakt 400 Zeilen und 51 Fachspalten nach erfolgreicher Validierung.~~ Nachweis: official-archive run: 400 rows and 51 `ideal_functions` columns.
- [x] ~~**A-090 – SSE-Berechnung implementieren.** Nach x ausgerichtet, vektorisiert mit Pandas, ohne vorzeitige Rundung.~~ Nachweis: `FunctionSelector.select` aligns by x and calculates unrounded vectorised Pandas SSE.
- [x] ~~**A-091 – Ideal-Funktionen auswählen.** Vier Ergebnisse einschließlich SSE und Maximalabweichung erzeugen; deterministische Tie-Regel anwenden.~~ Nachweis: official-archive run selects y13, y24, y36, and y40 with the documented values.
- [x] ~~**A-092 – Testpunkt-Mapper implementieren.** Punkte zeilenweise einlesen, alle vier Kandidaten prüfen, Mehrfachtrefferregel anwenden und Nichttreffer zählen.~~ Nachweis: `PointMapper` and `TestDataLoader`; official run yields 34 assigned and 66 unassigned points.
- [x] ~~**A-093 – Ergebnistabelle schreiben.** Ausschließlich erfolgreiche Zuordnungen mit `x`, `y`, `delta_y`, `ideal_function`; wiederholte x-Werte nicht verlieren.~~ Nachweis: SQLite check: `test_results` has x, y, delta_y, ideal_function and 34 successful rows.
- [x] ~~**A-094 – Laufzusammenfassung erzeugen.** Zeilenzahlen, gewählte Funktionen, SSE, Maximalabweichung, Grenzwerte, zugeordnete und nicht zugeordnete Punkte ausgeben.~~ Nachweis: `RunSummary`, console summary, and `output/run_summary.json`.
- [x] ~~**A-095 – Bokeh-Visualisierung implementieren.** Einheitliche Achsenbeschriftungen, Legende, Farb-/Symbolkodierung, Hover-Informationen und gut lesbare Skalierung.~~ Nachweis: `BokehVisualizer` creates panels, legend, colour/marker coding, axes, and hover fields.
- [x] ~~**A-096 – Große Wertebereiche berücksichtigen.** Darstellungen so aufteilen oder skalieren, dass kleine Funktionswerte nicht durch Funktionen mit sehr großen y-Werten unlesbar werden.~~ Nachweis: four separate Bokeh figures retain independent y-axis scaling.
- [x] ~~**A-097 – Abweichung sichtbar machen.** Abweichungen als Hover-Wert, Segment, separates Panel oder begründete Kombination darstellen; keine dekorative Grafik ohne Analysewert.~~ Nachweis: mapping hover fields and the separate assigned-deviation/threshold panel.
- [x] ~~**A-098 – Ausgabeformat implementieren.** Interaktives Bokeh-HTML reproduzierbar erzeugen; für die Arbeit zusätzlich hochwertige statische Exportabbildungen vorbereiten.~~ Nachweis: reproducible Bokeh HTML plus static-export guidance in `README.md`.
- [x] ~~**A-099 – Orchestrator/CLI implementieren.** Ein dokumentierter Befehl führt Validierung, Datenbankaufbau, Auswahl, Mapping und Visualisierung in korrekter Reihenfolge aus.~~ Nachweis: `ApplicationRunner`, `python -m ideal_function_assignment`, and console script.
- [x] ~~**A-100 – Logging implementieren.** Informative Statusmeldungen und aussagekräftige Fehler; keine Rohdatenflut und keine verschluckten Ausnahmen.~~ Nachweis: concise status/error logging in the runner and CLI.
- [x] ~~**A-101 – Docstrings vervollständigen.** Jedes Modul, jede öffentliche Klasse, Methode und Funktion mit Zweck, Parametern, Rückgabewert und relevanten Exceptions dokumentieren.~~ Nachweis: module, class, function, and public-method docstrings in the application package.
- [x] ~~**A-102 – Kommentare prüfen.** Nur nicht offensichtliche fachliche Entscheidungen kommentieren; veraltete oder den Code bloß wiederholende Kommentare entfernen.~~ Nachweis: implementation review: explanatory docstrings only; no redundant line-by-line comments.
- [x] ~~**A-103 – README vervollständigen.** Zweck, Voraussetzungen, Installation, Datenablage, Ausführung, Tests, Ausgaben, Architekturüberblick, Repository-Struktur und Troubleshooting.~~ Nachweis: completed installation, run, output, architecture, quality-check, and troubleshooting README.
- [x] ~~**A-104 – Keine Notebook-Abhängigkeit.** Hauptlösung als ausführbares Python-Paket/Programm; Notebook höchstens ergänzend und nicht als einzige reproduzierbare Umsetzung.~~ Nachweis: executable package entry point `src/ideal_function_assignment/__main__.py`.

**Abnahme Phase 5: erledigt.** Der vollständige Funktionsumfang ist implementiert; der erfolgreiche Lauf mit `data/dataset.zip` erzeugt ohne manuelle Zwischenschritte SQLite-Datenbank, Bokeh-HTML und JSON-Zusammenfassung. Nachweis: Commit `7e0afa9`, Ruff/pytest und offizielles Ergebnis-Orakel.

### Phase 6 – Tests, statische Qualität und technische Abnahme

- [ ] **A-105 – Loader-Unit-Tests.** Gültige Dateien, fehlende Datei, falsche Header, nichtnumerische Werte, NaN/Inf, leere Datei, doppelte x-Werte und unpassende x-Mengen.
- [ ] **A-106 – SSE-Unit-Test.** Kleine handrechenbare Fixture mit exakt erwarteten SSE-Werten.
- [ ] **A-107 – Auswahl-Unit-Tests.** Eindeutiges Minimum und Gleichstandsregel.
- [ ] **A-108 – Maximalabweichungs-Test.** Absolutbetrag und Maximum mit positiver und negativer Differenz prüfen.
- [ ] **A-109 – Mapping-Unit-Tests.** Punkt klar innerhalb, exakt auf und knapp außerhalb des `sqrt(2)`-Grenzwerts.
- [ ] **A-110 – Mehrfachtreffer-Test.** Mehrere zulässige Funktionen, Auswahl der kleinsten Abweichung und deterministischer Tie-Break.
- [ ] **A-111 – Nichttreffer-Test.** Kein Kandidat; Punkt bleibt unzugeordnet und wird korrekt gezählt.
- [ ] **A-112 – x-Fehler-Test.** Unbekannter x-Wert löst das dokumentierte Verhalten aus; keine stillschweigende Interpolation.
- [ ] **A-113 – Datenbank-Schema-Test.** Tabellen- und Spaltennamen, Typen, Constraints und vier Fachspalten der Ergebnistabelle prüfen.
- [ ] **A-114 – Datenbank-Inhaltstest.** Zeilenzahlen, wiederholte Test-x-Werte, gespeicherte Funktionsnummern und `delta_y >= 0` prüfen.
- [ ] **A-115 – Transaktions-/Rollback-Test.** Fehler während des Schreibens hinterlässt keinen widersprüchlichen Teilzustand.
- [ ] **A-116 – Visualisierungs-Test.** HTML-Ausgabe entsteht; erwartete Datenquellen, Serien, Achsentitel und Legenden sind vorhanden.
- [ ] **A-117 – CLI-End-to-End-Test.** Lauf aus leerem Ausgabeverzeichnis erzeugt alle erwarteten Artefakte und endet mit erfolgreichem Exit-Code.
- [ ] **A-118 – Reproduzierbarkeitstest.** Zwei Läufe mit identischen Eingaben ergeben identische fachliche Ergebnisse.
- [ ] **A-119 – Offiziellen Datensatz als Akzeptanztest ausführen.** Erwartete Auswahl nach unabhängiger Vorprüfung:

  | Training | Ideal | SSE | maximale Abweichung | Grenzwert × √2 |
  |---|---:|---:|---:|---:|
  | y1 | y13 | 34.0807075815 | 0.499221 | 0.7060051088 |
  | y2 | y24 | 33.4517609531 | 0.499000 | 0.7056925676 |
  | y3 | y36 | 35.5727003958 | 0.498943 | 0.7056119575 |
  | y4 | y40 | 34.9988748132 | 0.499779 | 0.7067942400 |

- [ ] **A-120 – Zuordnungsoracle prüfen.** Erwartungswert: 34 zugeordnete und 66 nicht zugeordnete Testpunkte; 33 Punkte besitzen genau einen zulässigen Kandidaten, ein Punkt besitzt zwei Kandidaten.
- [ ] **A-121 – Realen Mehrfachtreffer prüfen.** Für Testzeile 50 (nullbasiert), (x=-1{,}6\), (y=-8{,}079187\), qualifizieren y13 und y24; wegen geringerer Abweichung muss y24 gewählt werden.
- [ ] **A-122 – Vollständigkeitsinvariante prüfen.** 34 + 66 = 100; keine verlorenen oder doppelt bewerteten Eingabezeilen.
- [ ] **A-123 – Testabdeckung auswerten.** Ziel: sämtliche fachlichen Kernzweige zu 100 % und das Gesamtprojekt mit hoher, begründeter Abdeckung; Prozentwert nicht als Ersatz für sinnvolle Assertions verwenden.
- [ ] **A-124 – Linter/Formatter ausführen.** Keine offenen Fehler; bewusst unterdrückte Regeln einzeln begründen.
- [ ] **A-125 – Typprüfung ausführen, falls konfiguriert.** Keine ungeklärten Fehler in Kernmodulen.
- [ ] **A-126 – Warnungen bereinigen.** Deprecation-, Ressourcen- und Datenbankwarnungen prüfen; keine relevante Warnung ignorieren.
- [ ] **A-127 – Code-Review gegen Architektur durchführen.** Keine übergroßen Klassen, verdeckten Seiteneffekte, redundanten Berechnungen oder nur pro forma eingebauten OOP-Muster.
- [ ] **A-128 – Frischer-Clone-Test durchführen.** In einem neuen Verzeichnis anhand ausschließlich des README installieren und ausführen.

**Abnahme Phase 6:** Alle Tests und Qualitätsprüfungen sind grün; erwartete Ergebnisse wurden unabhängig verifiziert; der Clone-Test funktioniert.

### Phase 7 – Finale Ergebnisse, Tabellen und Abbildungen erzeugen

- [ ] **A-129 – Finalen Analyselauf kennzeichnen.** Commit-ID, Python-/Paketversionen, Datensatz-Hash und Zeitpunkt dokumentieren.
- [ ] **A-130 – Finale SQLite-Datei prüfen.** Tabellen mit SQL-Abfragen kontrollieren; Zeilenzahlen und Stichproben gegen Python-Ergebnisse vergleichen.
- [ ] **A-131 – Ergebnistabelle exportieren.** Gewählte Funktionen, SSE, maximale Abweichungen und Grenzwerte mit sinnvoller Rundung; Berechnung intern ungerundet lassen.
- [ ] **A-132 – Mapping-Ergebnis zusammenfassen.** Anzahl/Anteil zugeordnet und nicht zugeordnet sowie Verteilung über die vier Ideal-Funktionen berichten.
- [ ] **A-133 – Ausreißer und Grenzfälle inspizieren.** Punkte nahe Grenzwert, größtes `delta_y` und Mehrfachtreffer fachlich prüfen.
- [ ] **A-134 – Visualisierung auf Vollständigkeit prüfen.** Jede Trainingsreihe, jede gewählte Ideal-Funktion, sämtliche Testpunkte beziehungsweise deren Status und die Abweichung sind logisch repräsentiert.
- [ ] **A-135 – Statische Abbildungen exportieren.** Scharf, lesbare Schrift, keine abgeschnittenen Legenden, angemessene Farben auch bei Graustufen/Farbsehschwäche.
- [ ] **A-136 – Abbildungsquellen vorbereiten.** Für selbst erzeugte Darstellungen `Source: Own representation.` beziehungsweise bei Datenbezug eine konsistente, zutreffende Formulierung verwenden.
- [ ] **A-137 – Keine Ergebnisübertreibung.** Ergebnisse auf diesen Datensatz und das vorgeschriebene Kriterium begrenzen; den `sqrt(2)`-Faktor nicht als statistisches Konfidenzmaß darstellen.
- [ ] **A-138 – Ergebnis-Nachweispaket einfrieren.** Finale Tabellen, Abbildungen, Testbericht und Laufprotokoll für die Schreibphase versionieren.

**Abnahme Phase 7:** Jede Zahl und jede Abbildung der Arbeit lässt sich auf einen eindeutig dokumentierten Programmlauf zurückführen.

### Phase 8 – Dokumentgerüst und Vorseiten erstellen

- [ ] **A-139 – Dokumenttemplate anwenden.** Seitenformat, Ränder, Schrift, Zeilenabstand, Überschriften, Seitenzahlen und Absatzformat nach aktueller IU-Vorgabe.
- [ ] **A-140 – Deckblatt erstellen.** Offiziell erforderliche Angaben vollständig, keine Seitenzahl sichtbar, nicht im Inhaltsverzeichnis.
- [ ] **A-141 – Inhaltsverzeichnis automatisch erzeugen.** Überschriftsebenen korrekt und Seitennummern aktualisierbar.
- [ ] **A-142 – Abbildungsverzeichnis anlegen.** Nur tatsächlich verwendete und korrekt beschriftete Abbildungen.
- [ ] **A-143 – Tabellenverzeichnis anlegen.** Nur tatsächlich verwendete und korrekt beschriftete Tabellen.
- [ ] **A-144 – Abkürzungsverzeichnis anlegen.** Nur nicht allgemein bekannte und tatsächlich verwendete Abkürzungen; bei wenigen Abkürzungen gemäß IU-Format prüfen, ob es erforderlich ist.
- [ ] **A-145 – Hauptkapitel in finaler Reihenfolge anlegen.** Exakt die Struktur und das Budget aus Abschnitt 6 verwenden.
- [ ] **A-146 – Literaturverzeichnis-Platzhalter anlegen.** Automatisch oder kontrolliert manuell; keine unzitierten Einträge.
- [ ] **A-147 – Repository-Link-Platzhalter anlegen.** Später auf finalen Tag/Release beziehungsweise unveränderlichen Commit verweisen.
- [ ] **A-148 – Seitenzähler etablieren.** Nach jeder Schreibphase Seitenzahl von Introduction bis Conclusion protokollieren.

**Abnahme Phase 8:** Dokumentstruktur, Verzeichnisse, Formatvorlage und Seitenkontrolle funktionieren vor Beginn des Volltextes.

### Phase 9 – Arbeit Abschnitt für Abschnitt in finaler Reihenfolge schreiben

#### 1 Introduction

- [ ] **A-149 – Problemkontext einordnen.** Auswahl passender Funktionen aus Kandidaten und reproduzierbare Verarbeitung heterogener Daten als konkretes Problem erklären; keine beliebige Python-Einleitung.
- [ ] **A-150 – Relevanz begründen.** Bezug zu nachvollziehbarer Datenanalyse, deterministischer Auswahl und überprüfbarer Software herstellen und passend belegen.
- [ ] **A-151 – Forschungslücke/-interesse auf Assignment-Niveau formulieren.** Nicht künstlich eine globale Forschungslücke behaupten; das Erkenntnisinteresse liegt in der begründeten Umsetzung und Evaluation der vorgegebenen Kriterien.
- [ ] **A-152 – Forschungsfrage wörtlich nennen.** Genau eine Hauptfrage, die im Conclusion eindeutig beantwortet wird.
- [ ] **A-153 – Ziel und Ergebnisarten nennen.** Anwendung, Datenbank, Tests, Visualisierung und kritische Bewertung.
- [ ] **A-154 – Scope und Abgrenzung nennen.** Kandidatenauswahl statt Parameterschätzung; keine Prognose/Extrapolation.
- [ ] **A-155 – Vorgehen und zentrale Designentscheidungen skizzieren.** Least squares, Grenzwert, OOP, SQLite und Tests kurz positionieren, ohne Ergebnisse vorwegzunehmen.
- [ ] **A-156 – Aufbau der Arbeit beschreiben.** Leserführung durch die folgenden Kapitel.
- [ ] **A-157 – Introduction gegen 10-%-Kriterium prüfen.** Konkret, quellenbasiert, nicht bloß Wiederholung der Aufgabenstellung.

#### 2 Requirements and Theoretical Background

- [ ] **A-158 – Funktionale Anforderungen systematisieren.** Datenimport, Auswahl, Mapping, Speicherung, Visualisierung und Git-Aufgabe.
- [ ] **A-159 – Qualitätsanforderungen systematisieren.** OOP, Vererbung, Exceptions, Dokumentation, Tests und Reproduzierbarkeit.
- [ ] **A-160 – Datensatz knapp beschreiben.** Dateien, Dimensionen, x-Bereich, Datenqualität und wiederholte Test-x-Werte; Relevanz jedes Merkmals erklären.
- [ ] **A-161 – Least-squares/SSE theoretisch erklären.** Formel sauber setzen, Variablen definieren, fachliche Quelle mit Fundstelle nennen und Bezug zur Auswahl herstellen.
- [ ] **A-162 – Residuen/absolute Abweichung erklären.** Unterscheidung zwischen quadriertem Auswahlkriterium und absoluter Zuordnungsabweichung klar machen.
- [ ] **A-163 – `sqrt(2)`-Grenzwert erklären.** Als von der Aufgabe vorgeschriebene Entscheidungsregel darstellen; keine unbelegte statistische Interpretation.
- [ ] **A-164 – Nachvollziehbare Übergangslogik schreiben.** Theorie führt direkt zur Methodik; keine isolierte Lehrbuchsammlung.

#### 3 Methodology

- [ ] **A-165 – Gesamtprozess methodisch beschreiben.** Validieren → persistieren → auswählen → Grenzwerte bestimmen → Testpunkte zuordnen → speichern → visualisieren → prüfen.
- [ ] **A-166 – Datenvalidierungsmethode begründen.** Warum Schema-, Typ-, x- und Vollständigkeitsprüfungen für korrekte Funktionsvergleiche notwendig sind.
- [ ] **A-167 – Auswahlalgorithmus formal beschreiben.** SSE für alle 4 × 50 Kombinationen, unabhängiges Argmin und Tie-Regel.
- [ ] **A-168 – Mappingalgorithmus formal beschreiben.** x-genauer Funktionswert, absolute Abweichung, Grenzwert, Mehrfachtreffer und Nichttreffer.
- [ ] **A-169 – Persistenzmethode beschreiben.** Tabellenschemata, Transaktionen und zeilenweises Mapping; Bezug zur Aufgabenanforderung.
- [ ] **A-170 – Evaluationsmethode beschreiben.** Mathematische Oracles, Unit-/Integrations-/End-to-End-Tests und Vollständigkeitsinvariante.
- [ ] **A-171 – Visualisierungsmethode begründen.** Welche Kodierung welche analytische Frage beantwortet.
- [ ] **A-172 – Methodische Grenzen vorab benennen.** Kandidatenmenge und Grenzfaktor vorgegeben; keine Generalisierung über den Datensatz hinaus.

#### 4 System Design and Architecture

- [ ] **A-173 – Komponentenarchitektur darstellen.** Loader, Validator, Repository/Database, Selector, Mapper, Visualizer und Orchestrator mit klaren Verantwortlichkeiten.
- [ ] **A-174 – Vererbung begründen.** Gemeinsame Loader-Invarianten und spezialisierte Schemas; Nutzen und Grenze der Vererbung erklären.
- [ ] **A-175 – Datenfluss darstellen.** Architekturabbildung im Text referenzieren und erläutern.
- [ ] **A-176 – Datenbankschema darstellen.** Tabellen, Spalten, Schlüssel/Constraints und Umgang mit wiederholten Test-x-Werten.
- [ ] **A-177 – Exception-Strategie darstellen.** Technische Fehler in fachlich verständliche eigene Exceptions übersetzen und an der CLI-Grenze ausgeben.
- [ ] **A-178 – Alternativen abwägen.** Beispielsweise Vektorisierung versus zeilenweises Testmapping, Komposition versus Vererbung, SQLite versus In-Memory-only; Auswahl begründen.
- [ ] **A-179 – Testbarkeit als Designziel erklären.** Reine Rechenfunktionen, Dependency Injection/Pfadkonfiguration und kleine Verantwortlichkeiten.

#### 5 Implementation

- [ ] **A-180 – Umgebung und Pakete nennen.** Versionen reproduzierbar angeben; keine lange Bibliothekswerbung.
- [ ] **A-181 – Datenimport und Validierung erklären.** Relevante Umsetzung mit kurzem Ausschnitt nur bei analytischem Mehrwert.
- [ ] **A-182 – SQLAlchemy-/SQLite-Umsetzung erklären.** Schemaerzeugung, Transaktion und Schreibreihenfolge.
- [ ] **A-183 – SSE-Auswahl erklären.** Verbindung zwischen Formel, Pandas-Operation und Rückgabeobjekt.
- [ ] **A-184 – Testmapping erklären.** Line-by-line-Verarbeitung, Grenzvergleich, Mehrfachtreffer und Speicherung.
- [ ] **A-185 – Exception- und Logging-Umsetzung erklären.** Konkrete Fehlerpfade statt Aufzählung von Klassennamen.
- [ ] **A-186 – Bokeh-Umsetzung erklären.** Datenquellen, Glyphen, Panels und Abweichungsdarstellung.
- [ ] **A-187 – Testimplementierung erklären.** Repräsentative Tests und warum genau diese Randfälle Beweiskraft besitzen.
- [ ] **A-188 – Git-Zusatzaufgabe vollständig bearbeiten.** Im Text oder in einer kompakten Tabelle/Befehlsbox mindestens folgenden fachlichen Ablauf zeigen und erklären:

  ```bash
  git clone --branch develop --single-branch <repository-url>
  cd <repository-directory>
  git switch -c feature/<feature-name>
  git add <changed-files>
  git commit -m "Add <feature>"
  git push --set-upstream origin feature/<feature-name>
  ```

  Anschließend Pull Request von `feature/<feature-name>` nach `develop`, Review, gegebenenfalls Korrekturcommits und Merge beschreiben. Keine Zugangsdaten oder echte Tokens abdrucken.

- [ ] **A-189 – Repository-Verweis setzen.** URL und finalen Tag/Commit nennen; vollständigen Code nicht in das Dokument kopieren.
- [ ] **A-190 – Implementierungsabschnitt fokussieren.** Code nicht dateiweise nacherzählen; nur Entscheidungen erläutern, die Forschungsfrage und Bewertung tragen.

#### 6 Results and Analysis

- [ ] **A-191 – Datenvalidierungsergebnis berichten.** Dimensionen, x-Konsistenz, fehlende Werte und Testduplikate knapp mit Bedeutung.
- [ ] **A-192 – Ausgewählte Funktionen berichten.** y1→y13, y2→y24, y3→y36, y4→y40 zusammen mit SSE und Maximalabweichungen.
- [ ] **A-193 – Zuordnungsergebnis berichten.** Nach finalem Programmlauf 34/100 zugeordnet und 66/100 nicht zugeordnet verifizieren und analysieren.
- [ ] **A-194 – Mehrfachtreffer analysieren.** Den realen Doppel-Kandidaten als Nachweis für die notwendige Auswahlregel erläutern.
- [ ] **A-195 – Visualisierungen integrieren.** Jede Abbildung im Text vor oder unmittelbar nach ihrem Erscheinen ankündigen, analytisch lesen und interpretieren.
- [ ] **A-196 – Testergebnisse berichten.** Anzahl bestandener Tests, abgedeckte Kernfälle und technischer Reproduzierbarkeitstest; kein bloßes `all tests passed` ohne Bedeutung.
- [ ] **A-197 – Zahlenkonsistenz prüfen.** Tabelle, Fließtext, Abbildung, Datenbank und Repository-Ausgabe müssen dieselben Werte zeigen.
- [ ] **A-198 – Ergebnis von Interpretation trennen.** Erst Befund, dann Bedeutung; keine kausalen oder statistischen Behauptungen ohne Grundlage.

#### 7 Discussion

- [ ] **A-199 – Forschungsfrage anhand der Ergebnisse diskutieren.** Erklären, inwiefern Architektur und Methodik eine korrekte, reproduzierbare Lösung ermöglichen.
- [ ] **A-200 – Designstärken abwägen.** Determinismus, Trennung der Verantwortlichkeiten, Datenvalidierung, Transaktionen, Tests und Nachvollziehbarkeit.
- [ ] **A-201 – Designnachteile abwägen.** Zusätzliche OOP-Komplexität, Bindung an festes CSV-Schema, SQLite als lokale Lösung und Aufwand statischer Bokeh-Exporte.
- [ ] **A-202 – Methodische Grenzen diskutieren.** Vorgegebene Kandidaten und Schwelle, keine Parameterschätzung, keine Interpolation, datensatzspezifische Resultate, Empfindlichkeit gegenüber Extremwerten der maximalen Abweichung.
- [ ] **A-203 – Aussagegrenzen festhalten.** Keine Prognosegüte, keine Signifikanz und keine allgemeine Modellüberlegenheit behaupten.
- [ ] **A-204 – Alternativen kritisch einordnen.** Beispielsweise andere Abweichungsmaße oder normalisierte Kriterien nur als begrenzte Perspektive, nicht als neue unerledigte Aufgabenstellung.
- [ ] **A-205 – Praktische Reproduzierbarkeit bewerten.** Repository, Versionen, Datenplatzierung und automatisierte Tests als Teil des Ergebnisses reflektieren.

#### 8 Conclusion

- [ ] **A-206 – Forschungsfrage ausdrücklich beantworten.** Eine klare, auf die Ergebnisse gestützte Antwort formulieren.
- [ ] **A-207 – Zentrale Synthese liefern.** Methodik, technische Lösung und wichtigste Ergebnisse verbinden; Kapitel nicht nur wiederholen.
- [ ] **A-208 – Wichtigste Zahlen knapp nennen.** Ausgewählte Funktionen und Zuordnungsumfang nur soweit für die Antwort erforderlich.
- [ ] **A-209 – Limitierungen integrieren.** Die wichtigsten Grenzen mit Konsequenz für die Interpretation nennen.
- [ ] **A-210 – Vorsichtige Empfehlung/Perspektive formulieren.** Nur aus der Diskussion ableiten; kein neuer selbstständiger `Future Work`-Abschnitt.
- [ ] **A-211 – Keine neuen Quellen oder Argumente einführen.** Conclusion ist Synthese, nicht Erweiterung.
- [ ] **A-212 – Introduction–Conclusion-Spiegel prüfen.** Jede in der Introduction angekündigte Frage/Zielsetzung wird im Conclusion geschlossen.

#### Reference List

- [ ] **A-213 – Literaturverzeichnis automatisch/regelbasiert erzeugen.** Ein gemeinsames alphabetisches Verzeichnis, keine Trennung nach Quellentyp.
- [ ] **A-214 – Bidirektional prüfen.** Jede Textzitation hat genau einen passenden Eintrag; jeder Eintrag wird im Text tatsächlich verwendet.
- [ ] **A-215 – Metadaten prüfen.** Autorennamen, Jahr, Titel, Journal/Verlag, Band/Ausgabe, Seiten, DOI/URL und Veröffentlichungsstatus mit Originalquelle vergleichen.
- [ ] **A-216 – APA/IU-Format prüfen.** Sentence case, Kursivsetzung, alphabetische/chronologische Sortierung, 1,5-zeilig, zweite und folgende Zeile 1,27 cm eingerückt, keine Aufzählungszeichen.
- [ ] **A-217 – DOI/URL-Regel prüfen.** DOI bevorzugen; URL nur gemäß Zugänglichkeit und Quellentyp; kein Abrufdatum nach IU-Regel.
- [ ] **A-218 – Keine KI als Informationsquelle zitieren.** KI-Ausgaben sind keine wissenschaftliche Quelle; jede sachliche Behauptung auf Originalquellen zurückführen.

#### Anhänge und ergänzende Materialien

- [ ] **A-219 – Anhangsbedarf kritisch prüfen.** Kein vollständiger Codeanhang. Nur zwingend notwendige Materialien aufnehmen, die den Haupttext nicht ersetzen.
- [ ] **A-220 – Anhangsverzeichnis nur bei tatsächlichem Anhang.** Jeder Anhang im Text referenziert, betitelt und logisch nummeriert.
- [ ] **A-221 – Seitenlimit nicht umgehen.** Argumentativ notwendige Inhalte bleiben im 15-seitigen Haupttext.

**Abnahme Phase 9:** Alle vorgesehenen Kapitel sind vollständig, logisch verbunden, quellenbasiert und innerhalb des Seitenbudgets; Forschungsfrage, Methodik, Ergebnisse, Diskussion und Conclusion bilden einen geschlossenen Argumentationsbogen.

### Phase 10 – Zitations-, Plagiats-, Sprach- und Formprüfung

- [ ] **A-222 – Satz-für-Satz-Quellenprüfung.** Jede nicht selbst entwickelte Idee, Tatsachenbehauptung, Definition, Gleichung und fremde Argumentation auf Belegpflicht prüfen.
- [ ] **A-223 – IU-Fundstellenregel prüfen.** Bei Direktzitaten und auf bestimmte Passagen bezogenen Paraphrasen Autor, Jahr und Seite(n); bei werkweiter Paraphrase Autor und Jahr.
- [ ] **A-224 – Paraphrasen prüfen.** Inhalt wirklich in eigener Struktur und Sprache wiedergeben; kein bloßer Synonymaustausch oder Patchwriting.
- [ ] **A-225 – Lange Paraphrasen prüfen.** Quelle im ersten Satz eindeutig einführen; in neuem Absatz erneut nennen; Umfang der Quellenabhängigkeit sprachlich klar halten.
- [ ] **A-226 – Direktzitate minimieren.** Nur bei sprachlichem Eigenwert; bis 40 Wörter mit Anführungszeichen, über 40 Wörter als eingerücktes Blockzitat ohne Anführungszeichen.
- [ ] **A-227 – Übersetzungen prüfen.** Fremdsprachiges Direktzitat im Original, Übersetzung nach IU-Regel in Fußnote; eine Übersetzung ohne Quellenangabe ist ebenfalls Plagiat.
- [ ] **A-228 – Selbstplagiat ausschließen.** Keine früher eingereichten Text- oder Codeleistungen ohne zulässige Kennzeichnung/Abklärung übernehmen; keine Wiederverwendung einer bereits bewerteten Arbeit.
- [ ] **A-229 – Abbildungs-/Tabellenzitation prüfen.** Titel oberhalb, Quellenzeile unterhalb, korrekte Formulierung (`Own representation`, `Adapted from`, `Own representation based on`), gegebenenfalls Lizenz.
- [ ] **A-230 – Rechte prüfen.** Fremde Screenshots/Grafiken vermeiden oder Nutzungsrecht klären; selbst erzeugte Diagramme bevorzugen.
- [ ] **A-231 – KI-Nutzung regelkonform prüfen.** KI nur im nach IU-Regel zulässigen Umfang als Hilfsmittel; keine KI-Aussage ungeprüft übernehmen; bei KI-generierten Bildern Prompt und Tool offenlegen. Für diese Arbeit sind KI-Bilder nicht vorgesehen.
- [ ] **A-232 – Argumentationsprüfung je Absatz.** Hauptaussage am Absatzanfang, Begründung/Beleg, Analyse und Übergang zum nächsten Punkt.
- [ ] **A-233 – Wissenschaftlichen Stil prüfen.** Kein `I`/`you`, keine Umgangssprache, keine vagen Aussagen wie `very important`, keine unbegründeten Superlative.
- [ ] **A-234 – Redundanzprüfung durchführen.** Dieselbe Begründung nicht in Methodology, Implementation, Results und Discussion wiederholen; Funktion der Kapitel trennen.
- [ ] **A-235 – Terminologie vereinheitlichen.** `training function`, `ideal function`, `test point`, `SSE`, `absolute deviation`, `threshold`, `mapping` konsistent verwenden und beim ersten Auftreten definieren.
- [ ] **A-236 – Gleichungen prüfen.** Variablen definiert, Indizes konsistent, Nummerierung nur bei Textverweis, Satzzeichen und Quellen korrekt.
- [ ] **A-237 – Sprachprüfung durchführen.** Grammatik, Rechtschreibung, Interpunktion, Zeitformen und akademischer Ton; anschließend manuelle Kontrolle fachlicher Bedeutungsänderungen.
- [ ] **A-238 – Ähnlichkeitsprüfung einordnen.** Turnitin-Treffer qualitativ prüfen; korrekte Zitate und unvermeidbare Fachbegriffe von unzulässigen Übernahmen unterscheiden, nicht auf einen willkürlichen Prozentwert optimieren.

**Abnahme Phase 10:** Keine unbelegte Fremdaussage, kein ungeprüfter Literaturverweis, keine problematische Textübernahme und keine formale Zitationslücke verbleiben.

### Phase 11 – Rubrikbasierte Gesamtprüfung und finale technische Freigabe

- [ ] **A-239 – Introduction (10 %) bewerten.** Scope, Ziel, Forschungsinteresse/-frage, Vorgehen und Begründung vollständig und konkret.
- [ ] **A-240 – Structure (15 %) bewerten.** Linearer roter Faden, angemessene Kapitelgewichte, klare Übergänge, Methodik vor Implementierung.
- [ ] **A-241 – Reasoning (40 %) bewerten.** Jede Designentscheidung begründet, Alternativen abgewogen, Quellen passend, Resultate analysiert und Grenzen kritisch reflektiert.
- [ ] **A-242 – Conclusion (15 %) bewerten.** Forschungsfrage beantwortet, Synthese statt Wiederholung, Limitationen und vorsichtige Perspektive enthalten.
- [ ] **A-243 – Language/form (10 %) bewerten.** Präzise, wissenschaftliche Sprache; korrekte Orthografie und Zeichensetzung.
- [ ] **A-244 – Formalities (10 %) bewerten.** IU-Layout, Verzeichnisse, Zitierweise, Seitenumfang und Eigenständigkeitserklärung korrekt.
- [ ] **A-245 – Traceability-Matrix vollständig abhaken.** Jede offizielle Aufgabe besitzt Code, Test, Ergebnisnachweis und Textstelle gemäß Abschnitt 7.
- [ ] **A-246 – Repository bereinigen.** Keine Originaldaten, SQLite-Laufdateien, Caches, Geheimnisse, lokalen Pfade oder unnötigen Binärdateien.
- [ ] **A-247 – README-Blindtest.** Eine andere Person kann die Anwendung ohne mündliche Hilfe ausführen.
- [ ] **A-248 – Alle Qualitätsbefehle final ausführen.** Tests, Abdeckung, Linter, Formatter, Typprüfung und End-to-End-Lauf auf dem finalen Commit.
- [ ] **A-249 – Ergebnisse neu erzeugen.** Alle in der Arbeit verwendeten Zahlen und Abbildungen vom finalen Commit regenerieren.
- [ ] **A-250 – Repository-Version einfrieren.** Annotierten Tag, beispielsweise `submission-v1.0`, erstellen und zum Remote übertragen.
- [ ] **A-251 – Repository-Zugriff testen.** URL in privatem/abgemeldetem Kontext beziehungsweise mit Prüferberechtigung testen; Tag/Commit erreichbar.
- [ ] **A-252 – Commit-Konsistenz prüfen.** In der Arbeit genannter Tag/Commit entspricht exakt dem getesteten Stand.
- [ ] **A-253 – Dokumentverweise aktualisieren.** Inhalts-, Abbildungs- und Tabellenverzeichnis, Querverweise, Gleichungs- und Seitennummern aktualisieren.
- [ ] **A-254 – Seitenumfang messen.** Introduction bis Conclusion höchstens 15 Seiten; keine abgeschnittenen Sätze oder unlesbar verkleinerte Elemente.
- [ ] **A-255 – PDF erzeugen.** Schriften eingebettet, Links funktionsfähig, Abbildungen scharf, keine Umbruch-/Überlappungsfehler.
- [ ] **A-256 – PDF visuell Seite für Seite prüfen.** Deckblatt, Verzeichnisse, Überschriften, Tabellen, Abbildungen, Fußnoten, Seitenzahlen, Literaturverzeichnis und letzte Seite.
- [ ] **A-257 – PDF-Inhalt technisch prüfen.** Text durchsuchbar, keine fehlenden Zeichen, korrekte Metadaten, erwartete Seitenzahl und Dateigröße im Uploadlimit.
- [ ] **A-258 – Finale Zahlenprüfung.** Jede Kennzahl stichprobenartig gegen Datenbank/Programmausgabe; besonders 4 Auswahlfunktionen, SSE, 34/66 und Mehrfachtreffer.
- [ ] **A-259 – Finale Quellenprüfung.** DOI/URL öffnen, Fundstellen kontrollieren und Text-/Listenabgleich erneut durchführen.
- [ ] **A-260 – Freigabekopie sichern.** Finale PDF, Repository-Commit/Tag, Testbericht und Abgabenachweise unveränderlich archivieren.

**Abnahme Phase 11:** Inhalt, Technik, Repository, Quellen und PDF bilden einen konsistenten, reproduzierbaren finalen Stand ohne offene Punkte.

### Phase 12 – Turnitin-Abgabe und Nachweis sichern

- [ ] **A-261 – Elektronische Eigenständigkeitserklärung abgeben.** Vor dem Assignment-Upload gemäß myCampus abschließen.
- [ ] **A-262 – Deadline erneut prüfen.** Datum, Uhrzeit, Zeitzone und eventuelle Sperrfrist verifizieren; ausreichenden Zeitpuffer einplanen.
- [ ] **A-263 – Richtige finale Datei auswählen.** Dateiname, Version und Hash gegen Freigabekopie prüfen; keine Entwurfsdatei hochladen.
- [ ] **A-264 – PDF in Turnitin hochladen.** Nur über den vorgesehenen myCampus-Kurs.
- [ ] **A-265 – Upload-Vorschau prüfen.** Alle Seiten, Formeln, Abbildungen, Links und Sonderzeichen in der Plattformvorschau kontrollieren.
- [ ] **A-266 – Übermittlungsstatus prüfen.** Abgabe muss als erfolgreich/abgeschlossen markiert sein; bei Ersatzabgabe Regeln und Frist beachten.
- [ ] **A-267 – Bestätigung sichern.** Zeitstempel, Abgabe-ID/Quittung und final hochgeladene Datei lokal archivieren.
- [ ] **A-268 – Repository online belassen.** Prüferzugriff und im Dokument genannte Version während des gesamten Bewertungszeitraums unverändert verfügbar halten.
- [ ] **A-269 – Abschlussregister erstellen.** Abgabedatum, PDF-Hash, Repository-URL, Tag und Commit-ID gemeinsam dokumentieren.

**Abnahme Phase 12:** Turnitin bestätigt die richtige finale Datei; Eigenständigkeitserklärung und Repository-Zugriff sind nachweislich vollständig.

## 5. Technische Muss-Anforderungen und Abnahmenachweise

| Req-ID | Muss-Anforderung | Primärer Implementierungsnachweis | Testnachweis | Textstelle |
|---|---|---|---|---|
| T-01 | Vier Trainingsreihen, 50 Ideal-Funktionen und Testdaten einlesen | spezialisierte Loader | Loader-/Integrationstests | 2, 3, 5 |
| T-02 | SQLite-Datei selbstständig erzeugen | SQLAlchemy-Datenbankkomponente | Schema- und End-to-End-Test | 3–5 |
| T-03 | Training in einer Tabelle mit 5 Spalten speichern | `training_data` | Schema/400-Zeilen-Test | 4–5 |
| T-04 | Ideal-Funktionen in einer Tabelle mit 51 Spalten speichern | `ideal_functions` | Schema/400-Zeilen-Test | 4–5 |
| T-05 | Vier Ideal-Funktionen über minimale SSE auswählen | Selector | Rechen-, Tie- und Akzeptanztests | 2, 3, 5, 6 |
| T-06 | Größte absolute Trainingsabweichung je ausgewähltem Paar bestimmen | Selector-Ergebnis | Maximalabweichungs-Test | 2, 3, 6 |
| T-07 | Jeden Testpunkt zeilenweise prüfen | Test-Iterator/Mapper | 100-Punkte-Invariante | 3, 5, 6 |
| T-08 | `sqrt(2)`-Grenzwert einschließlich Gleichheit anwenden | Mapper | inside/boundary/outside | 2, 3, 5, 6 |
| T-09 | Mehrfachtreffer eindeutig auflösen | Minimum von `delta_y`, Tie-Break | künstlicher und realer Mehrfachtreffer | 3, 5–7 |
| T-10 | Erfolgreiche Zuordnung mit x, y, Delta y und Funktionsnummer speichern | `test_results` | Schema-/Inhaltstest | 4–6 |
| T-11 | Nicht zuordenbare Punkte korrekt behandeln | Zähler/Analyseausgabe | Nichttreffer-/Invarianztest | 3, 5–7 |
| T-12 | Alle Daten logisch visualisieren | Bokeh-Visualisierung | Struktur-/Exportprüfung | 3, 5, 6 |
| T-13 | Sinnvolle objektorientierte Architektur | Komponentenmodell | Code-Review/isolierte Tests | 4–5, 7 |
| T-14 | Mindestens eine sinnvolle Vererbung | Loader-Hierarchie | Loader-Polymorphietests | 4–5 |
| T-15 | Standard- und benutzerdefinierte Exceptions | Exception-Hierarchie | Fehlerpfadtests | 4–5 |
| T-16 | Pandas, Bokeh und SQLAlchemy sinnvoll verwenden | produktiver Code | Integration/End-to-End | 5–6 |
| T-17 | Nützliche Elemente testen | pytest-Suite | finaler Testbericht | 3, 5–6 |
| T-18 | Code vollständig dokumentieren | Docstrings/README | Docstring-/Review-Check | 5, Repository |
| T-19 | Git-Clone-, Commit-, Push-, PR- und Merge-Ablauf erklären | Git-Befehlsbox/Repository-Historie | Befehle fachlich geprüft | 5 |
| T-20 | Arbeit vollständig rekonstruierbar machen | README, Versionen, Tag, Repository-Link | frischer Clone | gesamte Arbeit |

## 6. Verbindliche Gliederung und Seitenbudget

Das Budget gilt für den Haupttext von der ersten Seite der Introduction bis zum Ende der Conclusion. Ziel sind etwa 14,5 Seiten; 0,5 Seite bleibt als Sicherheit gegen Layoutverschiebungen.

| Kapitel | Inhaltliche Funktion | Zielumfang | Harte Obergrenze |
|---|---|---:|---:|
| 1 Introduction | Kontext, Relevanz, Frage, Ziel, Scope, Vorgehen, Aufbau | 1,3 | 1,5 |
| 2 Requirements and Theoretical Background | Anforderungen, Daten, SSE, Abweichung, Grenzwert | 1,8 | 2,0 |
| 3 Methodology | Validierung, Auswahl, Mapping, Persistenz, Evaluation | 2,2 | 2,4 |
| 4 System Design and Architecture | OOP, Vererbung, Datenbank, Exceptions, Datenfluss | 1,8 | 2,0 |
| 5 Implementation | Kernumsetzung, Visualisierung, Tests, Git-Aufgabe, Repository | 2,0 | 2,2 |
| 6 Results and Analysis | Auswahl, Zuordnung, Visualisierungen, Testbefunde | 2,2 | 2,4 |
| 7 Discussion | Abwägung, Robustheit, Limitationen, Aussagegrenzen | 1,5 | 1,7 |
| 8 Conclusion | eindeutige Antwort und Synthese | 1,0 | 1,1 |
| **Gesamtziel** | | **13,8** | **15,0** |

Das Literaturverzeichnis folgt danach und wird gemäß der ausdrücklichen Projektentscheidung nicht in die 15 Inhaltsseiten eingerechnet. Es wird kein inhaltlich notwendiger Text in einen Anhang verschoben.

## 7. Geplante Abbildungen und Tabellen

Jedes Element wird nur aufgenommen, wenn es eine konkrete analytische Aufgabe erfüllt.

| Element | Zweck | Mindestinhalt | Quellenzeile |
|---|---|---|---|
| Fig. 1 – Processing and component architecture | Datenfluss und Verantwortlichkeiten verständlich machen | CSV, Loader/Validation, Selection/Mapping, SQLite, Bokeh | `Source: Own representation.` |
| Fig. 2 – Training and selected ideal functions with mapped test points | Visuelle Güte und Zuordnungen für alle vier Paare zeigen | vier lesbare Panels, Legende, Achsen, Teststatus | `Source: Own representation based on the provided dataset.` |
| Fig. 3 – Assignment deviations and threshold relation | Abweichungen und Grenzfalllogik analysieren | `delta_y`, Grenzwert, ggf. Status/Funktion | `Source: Own representation based on the provided dataset.` |
| Tab. 1 – Dataset and validation summary | Datenvertrag und Qualität belegen | Formen, x-Bereich, Fehlwerte, Duplikate | `Source: Own representation.` |
| Tab. 2 – Selected ideal functions | Kernergebnis kompakt belegen | Training, Ideal, SSE, max. Abweichung, Schwelle | `Source: Own representation.` |
| Tab. 3 – Test mapping summary | Zuordnungsumfang analysieren | pro Funktion, gesamt, nicht zugeordnet, Mehrfachtreffer | `Source: Own representation.` |
| Tab. 4 – Verification summary | Testbeweiskraft zeigen | Testebenen, Kernfälle, Ergebnis | `Source: Own representation.` |

Vor Aufnahme jedes Elements prüfen:

- [ ] Im Fließtext namentlich referenziert.
- [ ] Aussagekräftiger Titel statt Dateiname.
- [ ] Quellenzeile direkt darunter.
- [ ] Achsen, Einheit, Legende und Rundung erklärt.
- [ ] Ergebnis im Fließtext interpretiert.
- [ ] Keine Wiederholung derselben Information ohne zusätzlichen Erkenntniswert.
- [ ] Lesbar bei finaler PDF-Größe und in Graustufen.

## 8. Schreib- und Zitierregeln als laufende Qualitätsgates

### Bei jeder neuen Quelle

- [ ] Originaldokument geöffnet und relevante Passage selbst geprüft.
- [ ] Quelle wissenschaftlich zitierwürdig oder als offizielle technische Dokumentation geeignet.
- [ ] Metadaten und DOI/URL gegen Originalseite verifiziert.
- [ ] Exakte Fundstelle notiert.
- [ ] Konkrete Behauptung in der Quellenmatrix festgehalten.

### Bei jedem neuen Absatz

- [ ] Erste Aussage benennt den Hauptpunkt.
- [ ] Fremde Idee/Behauptung besitzt unmittelbar einen passenden Beleg.
- [ ] Quelle stützt exakt diese Aussage und nicht nur das allgemeine Thema.
- [ ] Eigene Analyse ist sprachlich von Quelleninhalt unterscheidbar.
- [ ] Absatz endet mit Schlussfolgerung oder nachvollziehbarem Übergang.
- [ ] Keine unnötige Wiederholung eines früheren Absatzes.

### Bei jeder Zitation

- [ ] Schreibweise des Autors entspricht dem Literaturverzeichnis.
- [ ] Ein Autor: Autor, Jahr, Fundstelle.
- [ ] Zwei Autoren: `and` narrativ, `&` in Klammern.
- [ ] Drei oder mehr: erster Autor + `et al.`.
- [ ] Mehrere Quellen in einer Klammer alphabetisch und mit Semikolon getrennt.
- [ ] Gleicher Autor/gleiches Jahr mit a, b, c konsistent aufgelöst.
- [ ] Seitenbereich mit `pp.` und korrektem Bereich; einzelne Seiten vollständig angegeben.
- [ ] Neuer Absatz mit fortgesetzter Paraphrase zitiert die Quelle erneut.

### Beim Literaturverzeichnis

- [ ] Alphabetisch, bei gleichem Autor chronologisch.
- [ ] Keine Aufzählungszeichen und keine Trennung nach Quellentyp.
- [ ] Titel in sentence case; Buch-/Journal-/Zeitungstitel korrekt kursiv.
- [ ] Bis 20 Autoren vollständig; ab 21 nach IU/APA-Regel.
- [ ] Institutionen ausgeschrieben.
- [ ] DOI bevorzugt; nur geeignete öffentliche URL, kein unnötiger Datenbank-Loginlink.
- [ ] Kein Abrufdatum.
- [ ] Hängender Einzug 1,27 cm und Zeilenabstand 1,5.

## 9. Finale Stop-Kriterien

Die Abgabe darf nicht erfolgen, solange mindestens einer dieser Punkte zutrifft:

- [ ] Eine offizielle technische Anforderung besitzt keinen Test oder Nachweis.
- [ ] Ein Testpunkt wird weder als zugeordnet noch als nicht zugeordnet erfasst.
- [ ] Der Mehrfachtreffer ist nicht deterministisch behandelt.
- [ ] Zahlen in Arbeit, Datenbank und Repository-Ausgabe widersprechen sich.
- [ ] Das Repository enthält nicht freigegebene Original-CSV-Dateien, Zugangsdaten oder lokale Pfade. Die unveränderte Datei `data/dataset.zip` ist die dokumentierte Ausnahme.
- [ ] Der Repository-Link ist für die prüfende Person nicht erreichbar.
- [ ] Der finale Commit wurde nach Erzeugung der berichteten Ergebnisse verändert.
- [ ] Eine Abbildung ist unlesbar, unbeschriftet, nicht referenziert oder nicht interpretiert.
- [ ] Eine fachliche Aussage hat keine geeignete Quelle/Fundstelle.
- [ ] Eine Quelle wurde nicht im Original geprüft oder könnte erfunden/fehlerhaft sein.
- [ ] Text und Literaturverzeichnis stimmen nicht bidirektional überein.
- [ ] Methodik/Design werden erst nach der Implementierung erklärt.
- [ ] Introduction enthält keine eindeutige Forschungsfrage oder Conclusion beantwortet sie nicht.
- [ ] Der Haupttext überschreitet 15 Seiten.
- [ ] PDF-Vorschau oder Turnitin-Vorschau weist Layout-/Zeichenfehler auf.
- [ ] Elektronische Eigenständigkeitserklärung oder Abgabebestätigung fehlt.

## 10. Änderungsprotokoll

| Datum | Änderung | Grund/Quelle | Auswirkung |
|---|---|---|---|
| 2026-09-01 | Initiale Masterliste erstellt | Projektquellen und Nutzerentscheidung | Verbindlicher Ablauf A-001 bis A-269 |
| 2026-09-01 | Seitenlimit auf 15 Inhaltsseiten ohne Literaturverzeichnis festgelegt | ausdrückliche Nutzerentscheidung | altes 15–20-Seiten-Ziel verworfen |
| 2026-09-01 | Vollständiger Code ausschließlich im Repository | ausdrückliche Nutzerentscheidung | Codeanhang entfällt; Repository-Nachweis wird Pflicht |
| 2026-09-01 | Originalarchiv versioniert, synthetische Fixtures verworfen | ausdrückliche Nutzerentscheidung | `data/dataset.zip` bleibt im Repository; entpackte CSV-Dateien bleiben ignoriert |
| 2026-09-03 | Phase-1-Baseline validiert | frische virtuelle Umgebung, pytest, Ruff und Paketimport | A-033 erledigt; technische Basis nachweisbar lauffähig |
| 2026-09-03 | Separate manuelle Datenprüfung entfernt | ausdrückliche Nutzerentscheidung „Der Datensatz ist korrekt“ | Datenvertrag statt Audit; A-035 bis A-042 und A-046 bewusst gestrichen |
| 2026-09-03 | Quellenmatrix angelegt und verifiziert | `docs/SOURCE_MATRIX.md` | Phase 3 erledigt; Quellen- und Fundstellenkontrollen vor dem Volltextentwurf verfügbar |
| 2026-09-03 | Methodik und Systemdesign festgelegt | `docs/METHODOLOGY_AND_DESIGN.md` | Phase 4 erledigt; Implementierung folgt festgelegten Regeln und Verantwortlichkeiten |
| 2026-09-03 | Phase-5-Anwendung implementiert und ausgeführt | Commit `7e0afa9`; offizielles versioniertes Archiv | Phase 5 erledigt: SQLite, Bokeh, JSON-Zusammenfassung und CLI erzeugen die verifizierten Ergebnisse y13/y24/y36/y40 sowie 34/66 Zuordnungen |
