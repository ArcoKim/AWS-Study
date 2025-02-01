# Test
## Gradle
``` yaml
name: Test Gradle App

on:
  pull_request:
    branches:
      - main
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up JDK 11
        uses: actions/setup-java@v4
        with:
          java-version: 17
          distribution: 'corretto'
      
      - name: Grant execute permission for gradlew
        run: chmod +x gradlew
      
      - name: Test with Gradle
        run: ./gradlew --info test
```