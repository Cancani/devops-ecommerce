# Branching und Merging

Modell
Trunk Based Development mit main und kurzlebigen Feature Branches.

Branches
- main: stabiler Hauptzweig
- feature/<kurzbeschreibung>: Änderungen und neue Funktionen
- hotfix/<kurzbeschreibung>: dringende Korrekturen
- release/<X.Y.Z>: nur bei Bedarf

Pull Requests
- Empfohlen für jede Änderung
- Mindestens 1 Review
- Squash Merge
- Branch nach Merge löschen

Konflikte
- Branch vor PR mit main abgleichen
- Konflikte im Editor lösen und erneut prüfen

Releases und Tags
- SemVer: MAJOR.MINOR.PATCH
- Tags auf main, z. B. v1.0.0
