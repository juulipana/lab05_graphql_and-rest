import sys
import os
from datetime import datetime
from typing import Any, List, Dict
import pandas as pd

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)

from experiment.rest.client_rest import RESTClient
from experiment.graphql.client_graphql import GraphQLClient
from experiment.scenarios.scenario_definitions import get_scenarios
from experiment.utils.logger import setup_logger, log_error
from experiment.utils.metrics import create_metric_record

REST_BASE_URL = "http://localhost:3000/api"
GRAPHQL_ENDPOINT = "http://localhost:3000/graphql"
NUM_ITERATIONS = 30

def exec_safe(fn, *args, logger, label: str, scenario: str, iteration: int) -> Dict[str, Any] | None:
    try:
        name, treatment, t_ms, s_bytes = fn(*args)
        logger.info(f"{scenario} [{label}] {iteration} → {t_ms:.2f}ms | {s_bytes} bytes")
        return create_metric_record(scenario, treatment, iteration, t_ms, s_bytes)
    except Exception as e:
        log_error(logger, scenario, treatment, iteration, e)
        return None

def rest_call(client: RESTClient, sc, i: int) -> tuple[str, str, float, int]:
    if sc.rest_method == "GET":
        _, t, s = client.get(sc.rest_endpoint, params=sc.rest_params)
        return sc.name, "REST", t, s
    _, t, s = client.post(sc.rest_endpoint, params=sc.rest_params)
    return sc.name, "REST", t, s

def gql_call(client: GraphQLClient, sc, i: int) -> tuple[str, str, float, int]:
    _, t, s = client.execute_query(sc.graphql_query, variables=sc.graphql_variables)
    return sc.name, "GraphQL", t, s

def run_experiment():
    logger = setup_logger("experiment_runner")
    scenarios = get_scenarios()
    rest_client = RESTClient(REST_BASE_URL)
    graphql_client = GraphQLClient(GRAPHQL_ENDPOINT)
    records: List[Dict[str, Any]] = []
    for sc in scenarios:
        for i in range(1, NUM_ITERATIONS + 1):
            r = exec_safe(rest_call, rest_client, sc, i, logger=logger, label="REST", scenario=sc.name, iteration=i)
            if r: records.append(r)
            g = exec_safe(gql_call, graphql_client, sc, i, logger=logger, label="GraphQL", scenario=sc.name, iteration=i)
            if g: records.append(g)
    df = pd.DataFrame(records)
    out_dir = os.path.join(ROOT, "experiment", "results")
    os.makedirs(out_dir, exist_ok=True)
    file = os.path.join(out_dir, f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
    df.to_csv(file, index=False)
    logger.info(df.groupby(["scenario", "treatment"]).agg({
        "response_time_ms": ["mean", "std", "min", "max"],
        "response_size_bytes": ["mean", "std", "min", "max"]
    }))
    rest_client.close()
    graphql_client.close()

if __name__ == "__main__":
    run_experiment()
