# Mobile

Machine d'origine : Flutter 3.47.7 stable, Dart 3.13.5, dans `~/Libs/flutter`. Android Studio fournit le JDK (OpenJDK 25) et le SDK dans `~/Library/Android/sdk`. Xcode est installé pour iOS. `adb` est sur le PATH.

## Organisation

```text
~/My_Projects/Flutter/Apps        # applications
~/My_Projects/Flutter/Packages    # packages locaux (ex. video_visibility_detector)
```

## Socle le plus fréquent

Relevé dans les `pubspec.yaml` présents :

| Brique | Où elle apparaît |
| --- | --- |
| `flutter_riverpod` / `riverpod` | presque toutes les apps actives |
| `go_router` | el_professor, give_track, omniflow, pilotage_pro, read_beat, santelink_plus |
| `firebase_core` | aog_hymns_app, el_professor, fgm_lyrics_app, give_track, pilotage_pro |
| `freezed` | give_track |
| Shorebird | fgm_lyrics_app |

Le skill `riverpod-3-migration` (`~/.agents/skills`) sert à passer un ancien Riverpod vers 3.x sans réécriture aveugle : audit des providers, `ref`, puis validation.

Règles du langage : famille `dart-*.mdc` (style, patterns, sécurité, tests, hooks). React Native a sa propre famille `react-native-*.mdc` pour les projets Expo, y compris accessibilité et production readiness. Les apps du dossier Flutter sont en Dart, pas en React Native.

## Boucle quotidienne

```bash
flutter pub get
flutter analyze
flutter test
flutter run
```

Device : simulateur Xcode, émulateur Android, ou mobile-mcp. Parcours répétables : flows Maestro dans le dépôt, lancés avec le CLI `maestro` 2.x.

Correctifs hors store, seulement pour les apps déjà configurées : Shorebird.

Publication store : fastlane (Homebrew) et CocoaPods pour les plugins iOS.

## Règles Dart qui comptent tous les jours

La famille `dart-*.mdc` étend les règles communes. En pratique :

- état immuable, providers Riverpod comme source de vérité
- pas de secret Firebase dans un dépôt public (les fichiers de config plateforme restent hors Git ou sont restreints)
- tests widget et unitaires avant de déclarer un écran fini
- migration Riverpod par le skill dédié, pas par un remplacement global

## Apps locales au moment du dernier inventaire

La liste à jour est dans [Projets](../generated/projets.md). Noms vus sous `Flutter/Apps` : `aog_hymns_app`, `cash_loud`, `el_professor`, `empire-audition` (Nuxt, pas Flutter), `fgm_lyrics_app`, `give_track`, `harmony_forge`, `omniflow`, `pilotage_pro`, `read_beat`, `ryder`, `santelink_plus`.

Dépôts publics liés : `ido_prime`, `give_track`, `fgm_hymnals_apk` (APK seulement, sources privées), `flutter_project_setup`, `i18n_ai_extract`.
