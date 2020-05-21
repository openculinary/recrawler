# RecipeRadar Recrawler

The RecipeRadar recrawler exists to improve the coverage of recipe search results provided to users.

When a user searches for a set of ingredients, they may or may not find results depending on the recipes available in the search engine at the time.

The recrawler accepts a list of ingredients as input, and performs a real-time web search using [DuckDuckGo](https://duckduckgo.com) to retrieve a list of potentially relevant search results - which in the ideal case will include some recipes.

Web pages found by the recrawler are passed to the crawling interface of the [api](https://www.github.com/openculinary/api) service which will attempt to retrieve them for inclusion in the search engine.

## Install dependencies

Make sure to follow the RecipeRadar [infrastructure](https://www.github.com/openculinary/infrastructure) setup to ensure all cluster dependencies are available in your environment.

## Development

To install development tools and run linting and tests locally, execute the following commands:

```sh
$ pipenv install --dev
$ make lint tests
```

## Local Deployment

To deploy the service to the local infrastructure environment, execute the following commands:

```sh
$ make
$ make deploy
```
