#! /bin/sh

./wait-for-it.sh $PG_HOST:$PG_PORT -t 60

./wait-for-it.sh $ELASTICSEARCH_HOST:$ELASTICSEARCH_PORT -t 60

./wait-for-it.sh $REDIS_HOST:$REDIS_PORT -t 60

EXAMPLE_DIR="examples/projects"
echo "schema.py started"
python $EXAMPLE_DIR/schema.py --config $EXAMPLE_DIR/schema.json
echo "schema.py done"
# python $EXAMPLE_DIR/data.py --config $EXAMPLE_DIR/schema.json

bootstrap --config $EXAMPLE_DIR/schema.json
echo "bootstrap done"

pgsync --config $EXAMPLE_DIR//schema.json --daemon