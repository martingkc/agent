from .imports import *
from .. import tools_bp
from flask import Blueprint, jsonify, request


openapi_spec = {
    "openapi": "3.0.0",
    "info": {
        "title": "Agent Tools API",
        "version": "1.0.0"
    },
    "paths": {
        "http://localhost:5000/tools": {
            "get": {
                "summary": "Get list of tools",
                "responses": {
                    "200": {
                        "description": "List of tools",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "tools": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "name": {"type": "string"},
                                                    "description": {"type": "string"},
                                                    "method": {"type": "string"},
                                                    "endpoint": {"type": "string"},
                                                    "parameters": {"type": "array"}
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "http://localhost:5000/power": {
            "get": {
                "summary": "Calculate power of a number",
                "parameters": [
                    {
                        "name": "base",
                        "in": "query",
                        "required": True,
                        "schema": {
                            "type": "number"
                        }
                    },
                    {
                        "name": "exponent",
                        "in": "query",
                        "required": True,
                        "schema": {
                            "type": "number"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Calculated result",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "base": {"type": "number"},
                                        "exponent": {"type": "number"},
                                        "result": {"type": "number"}
                                    }
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "Missing required query parameters"
                    },
                    "500": {
                        "description": "Internal server error"
                    }
                }
            }
        },
        "http://localhost:5000/plot": {
            "post": {
                "summary": "Plot points and save as PNG",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "points": {
                                        "type": "array",
                                        "items": {
                                            "type": "array",
                                            "minItems": 2,
                                            "maxItems": 2,
                                            "items": {
                                                "type": "number"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "URL of the saved PNG file",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "url": {"type": "string"}
                                    }
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "No points provided"
                    }
                }
            }
        },
        "http://localhost:5000/wiki-summary": {
            "get": {
                "summary": "Fetch summary of a Wikipedia topic",
                "parameters": [
                    {
                        "name": "topic",
                        "in": "query",
                        "required": True,
                        "schema": {
                            "type": "string"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Summary of the topic",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "topic": {"type": "string"},
                                        "summary": {"type": "string"}
                                    }
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "Missing required query parameter 'topic'"
                    },
                    "500": {
                        "description": "Internal server error"
                    }
                }
            }
        },
        "http://localhost:5000/relevant-articles": {
            "post": {
                "summary": "Fetch relevant articles from the database based on query",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "query": {"type": "string"}
                                }
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "List of relevant articles",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "articles": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "title": {"type": "string"},
                                                    "content": {"type": "string"}
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "No query provided"
                    }
                }
            }
        },
        "http://localhost:5000/stock-data": {
            "get": {
                "summary": "Fetch historical stock data for Apple",
                "parameters": [
                    {
                        "name": "year",
                        "in": "query",
                        "required": True,
                        "schema": {
                            "type": "integer"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Stock price vs volume graph saved as HTML",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "url": {"type": "string"}
                                    }
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "Missing required query parameter 'year'"
                    },
                    "500": {
                        "description": "Internal server error"
                    }
                }
            }
        }
    }
}

@tools_bp.route('/hello', methods=['GET'])
def hello():
    """Return the OpenAPI JSON"""
    return jsonify('hello')

@tools_bp.route('/tools', methods=['GET'])
def get_tools():
    """Return the OpenAPI JSON"""
    return jsonify(openapi_spec)

@tools_bp.route('/power', methods=['GET'])
def calculate_power():
    '''Calculate the power of a number.
    Query Parameters:
    - base (float): The base number.
    - exponent (float): The exponent to raise the base to.

    Returns:
    - JSON response with the result of base raised to the power exponent.
    '''
    try:
        base = request.args.get('base', type=float)
        exponent = request.args.get('exponent', type=float)
        if base is None or exponent is None:
            return jsonify({'error': 'Missing required query parameters base and exponent'}), 400
        result = base ** exponent
        return jsonify({'base': base, 'exponent': exponent, 'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tools_bp.route('/plot', methods=['POST'])
def plot_points():
    '''Plot points on a graph and save as a PNG file.
    Request Body:
    - points (list): A list of points where each point is a tuple (x, y).

    Returns:
    - JSON response with the URL of the saved PNG file.
    '''
    data = request.json
    points = data.get('points', [])

    if not points:
        return jsonify({'error': 'No points provided'}), 400

    x, y = zip(*points)

    plt.scatter(x, y)
    plt.savefig('points_plot.png')
    plt.close()

    return jsonify({'url': 'http://localhost:5000/points_plot.png'})

@tools_bp.route('/wiki-summary', methods=['GET'])
def fetch_wiki_summary():
    """Fetch summary of a Wikipedia topic."""
    topic = request.args.get('topic')
    if not topic:
        return jsonify({'error': 'Missing required query parameter "topic"'}), 400
    
    try:
        url = f'https://en.wikipedia.org/api/rest_v1/page/summary/{topic}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            summary = data.get('extract', '')
            return jsonify({'topic': topic, 'summary': summary})
        else:
            return jsonify({'error': 'Error fetching summary from Wikipedia'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tools_bp.route('/relevant-articles', methods=['POST'])
def fetch_relevant_articles():
    '''Fetch relevant articles from the database.
    Request Body:
    - query (string): The query for searching relevant articles.

    Returns:
    - JSON response with the list of relevant articles.
    '''
    data = request.json
    query = data.get('query')

    if not query:
        return jsonify({'error': 'No query provided'}), 400

    try:
        # Load the chroma database
        db_client = Client('./chroma_db')
        embedding_model = OpenAI(model="text-embedding-small")

        # Get the embeddings for the query
        query_embedding = embedding_model.embed([query])

        # Fetch the top 10 relevant articles from the database
        top_articles = db_client.query(collection="articles", query=query_embedding, n_results=10)

        return jsonify({'articles': top_articles})
    except Exception as e:
        return jsonify({'error': str(e)}), 500