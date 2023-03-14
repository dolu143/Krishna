{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyMY+WxJutPQagEqzkYGeMm/",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/dolu143/Krishna/blob/main/credentials.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "!pip install smartapi-python\n",
        "!pip install websocket-client\n",
        "!pip install pyotp\n",
        "!git clone https://github.com/dolu143/Krishna.git"
      ],
      "metadata": {
        "id": "KHpPY2pa4RU3"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "from Krishna import functions"
      ],
      "metadata": {
        "id": "cT3MkeLVmbEg"
      },
      "execution_count": 1,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "functions.intializeSymbolTokenMap()\n",
        "tokenInfo = functions.getTokenInfo('NFO','OPTIDX','NIFTY',17000,'PE').iloc[0]\n",
        "#print(tokenInfo)\n",
        "symbol  = tokenInfo['symbol']\n",
        "token = tokenInfo['token']\n",
        "lot = int(tokenInfo['lotsize'])\n",
        "print(symbol, token, lot)"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "3qRpndLf4088",
        "outputId": "16537b90-6c81-4b53-a019-fbca7041b91c"
      },
      "execution_count": 2,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "NIFTY16MAR2317000PE 55582 50\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "functions.login()"
      ],
      "metadata": {
        "id": "-9TBYPal-ZNB",
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "outputId": "40a8e52d-018a-4b12-c953-0f24959a209d"
      },
      "execution_count": 3,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "0868101428\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "functions.place_order(token,symbol,lot,'NFO','BUY','MARKET',0)"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "Efe5yKSN6EPk",
        "outputId": "479509ca-c37a-4cae-d211-37e22e0007c2"
      },
      "execution_count": 4,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "The order id is: 230314001109105\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "functions.logout()"
      ],
      "metadata": {
        "id": "psXQ25yUo0vM",
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "outputId": "f8112f1b-2f56-4451-9f00-4b1c3cfea9f9"
      },
      "execution_count": 5,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Your Session was Logout Successfully\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [],
      "metadata": {
        "id": "b1ldd8Rk9eke"
      },
      "execution_count": 5,
      "outputs": []
    }
  ]
}