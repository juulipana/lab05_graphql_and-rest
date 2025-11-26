"""
Script principal para execução do experimento GraphQL vs REST.

Este script executa medições de desempenho comparando APIs REST e GraphQL
em diferentes cenários de consulta. Cada cenário é executado múltiplas vezes
para garantir validade estatística.

Instruções de execução:
    python runner/run_experiment.py

Ou, a partir da raiz do projeto:
    python -m experiment.runner.run_experiment

Configuração:
    - Número de iterações por cenário: 30 (padrão)
    - Resultados salvos em: experiment/results/results_YYYYMMDD_HHMMSS.csv
"""

import sys
import os
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from experiment.rest.client_rest import RESTClient
from experiment.graphql.client_graphql import GraphQLClient
from experiment.scenarios.scenario_definitions import get_scenarios
from experiment.utils.logger import setup_logger, log_experiment_start, log_experiment_end, log_error
from experiment.utils.metrics import create_metric_record


REST_BASE_URL = "http://localhost:3000/api"
GRAPHQL_ENDPOINT = "http://localhost:3000/graphql"
NUM_ITERATIONS = 30


def run_rest_scenario(client: RESTClient, scenario, iteration: int, logger) -> Dict[str, Any]:
    log_experiment_start(logger, scenario.name, "REST", iteration)
    
    try:
        if scenario.rest_method == "GET":
            result, response_time_ms, response_size_bytes = client.get(
                scenario.rest_endpoint,
                params=scenario.rest_params
            )
        else:
            result, response_time_ms, response_size_bytes = client.post(
                scenario.rest_endpoint,
                params=scenario.rest_params
            )
        
        log_experiment_end(logger, scenario.name, "REST", iteration, 
                          response_time_ms, response_size_bytes)
        
        return create_metric_record(
            scenario.name,
            "REST",
            iteration,
            response_time_ms,
            response_size_bytes
        )
    except Exception as e:
        log_error(logger, scenario.name, "REST", iteration, e)
        raise


def run_graphql_scenario(client: GraphQLClient, scenario, iteration: int, logger) -> Dict[str, Any]:
    log_experiment_start(logger, scenario.name, "GraphQL", iteration)
    
    try:
        result, response_time_ms, response_size_bytes = client.execute_query(
            scenario.graphql_query,
            variables=scenario.graphql_variables
        )
        
        log_experiment_end(logger, scenario.name, "GraphQL", iteration,
                          response_time_ms, response_size_bytes)
        
        return create_metric_record(
            scenario.name,
            "GraphQL",
            iteration,
            response_time_ms,
            response_size_bytes
        )
    except Exception as e:
        log_error(logger, scenario.name, "GraphQL", iteration, e)
        raise


def run_experiment():
    logger = setup_logger("experiment_runner")
    
    logger.info("=" * 80)
    logger.info("Iniciando experimento GraphQL vs REST")
    logger.info(f"Número de iterações por cenário: {NUM_ITERATIONS}")
    logger.info(f"REST Base URL: {REST_BASE_URL}")
    logger.info(f"GraphQL Endpoint: {GRAPHQL_ENDPOINT}")
    logger.info("=" * 80)
    
    scenarios = get_scenarios()
    logger.info(f"Total de cenários: {len(scenarios)}")
    
    rest_client = RESTClient(REST_BASE_URL)
    graphql_client = GraphQLClient(GRAPHQL_ENDPOINT)
    
    results = []
    
    try:
        for scenario in scenarios:
            logger.info(f"\n{'=' * 80}")
            logger.info(f"Processando cenário: {scenario.name}")
            logger.info(f"Descrição: {scenario.description}")
            logger.info(f"{'=' * 80}\n")
            
            for iteration in range(1, NUM_ITERATIONS + 1):
                try:
                    rest_result = run_rest_scenario(rest_client, scenario, iteration, logger)
                    results.append(rest_result)
                except Exception as e:
                    logger.error(f"Falha na execução REST - Iteração {iteration}: {str(e)}")
                
                try:
                    graphql_result = run_graphql_scenario(graphql_client, scenario, iteration, logger)
                    results.append(graphql_result)
                except Exception as e:
                    logger.error(f"Falha na execução GraphQL - Iteração {iteration}: {str(e)}")
        
        logger.info(f"\n{'=' * 80}")
        logger.info("Experimento concluído")
        logger.info(f"Total de medições coletadas: {len(results)}")
        logger.info(f"{'=' * 80}\n")
        
        df = pd.DataFrame(results)
        
        results_dir = os.path.join(os.path.dirname(__file__), '..', 'results')
        os.makedirs(results_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(results_dir, f"results_{timestamp}.csv")
        
        df.to_csv(output_file, index=False)
        logger.info(f"Resultados salvos em: {output_file}")
        
        logger.info("\nResumo estatístico:")
        logger.info(df.groupby(['scenario', 'treatment']).agg({
            'response_time_ms': ['mean', 'std', 'min', 'max'],
            'response_size_bytes': ['mean', 'std', 'min', 'max']
        }))
        
    finally:
        rest_client.close()
        graphql_client.close()
        logger.info("Conexões fechadas")


if __name__ == "__main__":
    run_experiment()

