from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class Scenario:
    name: str
    description: str
    rest_endpoint: str
    rest_method: str
    rest_params: Dict[str, Any]
    graphql_query: str
    graphql_variables: Dict[str, Any]


def get_scenarios() -> List[Scenario]:
    scenarios = [
        Scenario(
            name="simple_user",
            description="Obter um único usuário por ID",
            rest_endpoint="/users/1",
            rest_method="GET",
            rest_params={},
            graphql_query="""
            query GetUser($userId: ID!) {
                user(id: $userId) {
                    id
                    name
                    email
                }
            }
            """,
            graphql_variables={"userId": "1"}
        ),
        Scenario(
            name="user_with_posts",
            description="Obter um usuário e seus posts",
            rest_endpoint="/users/1",
            rest_method="GET",
            rest_params={"include": "posts"},
            graphql_query="""
            query GetUserWithPosts($userId: ID!) {
                user(id: $userId) {
                    id
                    name
                    email
                    posts {
                        id
                        title
                        content
                        createdAt
                    }
                }
            }
            """,
            graphql_variables={"userId": "1"}
        ),
        Scenario(
            name="user_posts_comments",
            description="Obter um usuário, seus posts e comentários de cada post",
            rest_endpoint="/users/1",
            rest_method="GET",
            rest_params={"include": "posts,posts.comments"},
            graphql_query="""
            query GetUserWithPostsAndComments($userId: ID!) {
                user(id: $userId) {
                    id
                    name
                    email
                    posts {
                        id
                        title
                        content
                        createdAt
                        comments {
                            id
                            content
                            author {
                                id
                                name
                            }
                            createdAt
                        }
                    }
                }
            }
            """,
            graphql_variables={"userId": "1"}
        )
    ]
    
    return scenarios


def get_scenario_by_name(name: str) -> Scenario:
    scenarios = get_scenarios()
    for scenario in scenarios:
        if scenario.name == name:
            return scenario
    raise ValueError(f"Scenario '{name}' not found")

