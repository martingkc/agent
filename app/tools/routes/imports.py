import matplotlib.pyplot as plt
import os
import uuid
import requests
from flask import Blueprint, jsonify, request
from openai import OpenAI
from chromadb import Client
import yfinance as yf
import plotly.graph_objs as go
