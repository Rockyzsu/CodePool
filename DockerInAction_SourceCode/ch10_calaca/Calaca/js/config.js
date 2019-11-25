/*
 * Calaca - Search UI for Elasticsearch
 * https://github.com/romansanchez/Calaca
 * http://romansanchez.me
 * @rooomansanchez
 * 
 * v1.2.0
 * MIT License
 */

/* Configs */
/**
 *
 * url - Cluster http url
 * index_name - Index name or comma-separated list
 * type - Type
 * size - Number of results to display at a time when pagination is enabled.
 * search_delay - Delay between actual search request in ms. Reduces number of queries to cluster by not making a request on each keystroke. 
 */

/*
* the cluster URL needs to be localhost for the example because this is a front-end only solution.
*/
var CALACA_CONFIGS = {
	url: "http://localhost:9200",
	index_name: "registry-events",
	type: "event",
	size: 10,
	search_delay: 500
}
