# Koalas

[![Koala](koala.jpg)](http://en.wikipedia.org/wiki/Koala)

Koalas is a singleton server for Pandas `DataFrame`s.

## Endpoints

 - `POST /dataframe`: load a new dataframe into the server. Most common is CSV,
   but JSON and HTML tables are also accepted. Set the "`Content-Type`" header
   to control parsing, and add additional args on the querystring (which will
   be passed to Pandas)
 
   Example: `curl -X POST http://localhost:5000/dataframe -H "Content-Type: text/csv" --data-binary @filename.csv`

 - `POST /query`: query an already loaded dataframe, using a pipeline of
   transformations. The format of the query looks something like this:
 
   ```
   curl -X POST http://localhost:5000/query \
        -H "Accept: text/csv" \
        -H "Content-Type: application/json" \
        -d '[{"name": "select", "fields": ["one", "two", "three"]}]',
   ```
 
## Transformations

The transformation pipeline is a JSON array of JSON objects, which requires a
`name` attribute (which is matched to one of the operation names below) and
accepts other named arguments as documented:

 - `select`: takes `fields` argument, returns new frame with only those fields
   selected
 - `slice`: takes `lower`, `upper`, and `step` which are analagous to Python's
   slice
 - `lt`, `lte`, `gt`, `gte`, `eq`, `ne`: take a `field` and `value` argument to
   filter data
 - `groupby`: same as Pandas' `groupby` operation, it requires `fields` (which
   can be a string or list) and optionally accepts the same named arguments
   `DataFrame.groupby` does.
 - `sum`, `mean`, and `medium`: perform operation on a grouped set
 - `resample`: resample the dataframe. `rule` and `how` are required (and take
   the same format as in Pandas) and all other named options to
   `DataFrame.resample` are accepted.
 - `localize`: localize a `DateTimeIndex` object into a new timezone - this
   will call `tz_convert` or `tz_localize` as appropriate. In the case where
   you want to convert from one timezone to another, first localize into the
   source timezone then the destination.
 - `plot`: takes the same named arguments as `DataFrame.plot`. The `Accept`
   header **must** be `image/png` if this is used, and it should be the last
   operation in the pipeline.
 
## Docker Image

A [trusted build](https://index.docker.io/help/docs/#trustedbuilds) of Kaoals is available at [brianhicks/koalas](https://index.docker.io/u/brianhicks/koalas/)

## But... Koalas?

Yeah, sure. I know Koalas aren't technically bears but they're pretty cool
Marsupials and there's nothing quite like them. Plus [they do
this](https://www.youtube.com/watch?v=H2cJAXyOKfU).
