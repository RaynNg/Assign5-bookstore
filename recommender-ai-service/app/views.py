from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import CustomerPreference
import requests
import random

BOOK_SERVICE_URL = "http://book-service:8000"
COMMENT_RATE_SERVICE_URL = "http://comment-rate-service:8000"
ORDER_SERVICE_URL = "http://order-service:8000"


@api_view(["GET"])
def api_index(request):
    """API Index - List all available endpoints"""
    return Response(
        {
            "service": "Recommender AI Service",
            "version": "1.0",
            "endpoints": {
                "GET /recommendations/customer/<customer_id>/": "Get AI recommendations for customer",
                "GET /recommendations/similar/<book_id>/": "Get similar books",
                "GET /recommendations/popular/": "Get popular books",
                "GET /recommendations/trending/": "Get trending books",
            },
        }
    )


class RecommendForCustomer(APIView):
    """
    AI-based recommendations for a specific customer
    Based on their purchase history, ratings, and preferences
    """

    def get(self, request, customer_id):
        try:
            # Get all books
            books_response = requests.get(f"{BOOK_SERVICE_URL}/books/")
            all_books = (
                books_response.json() if books_response.status_code == 200 else []
            )

            if not all_books:
                return Response({"recommendations": [], "reason": "No books available"})

            # Get customer preferences
            preference, _ = CustomerPreference.objects.get_or_create(
                customer_id=customer_id
            )
            purchased_books = preference.purchased_books or []

            # Filter out already purchased books
            available_books = [b for b in all_books if b["id"] not in purchased_books]

            # Simple recommendation: shuffle and return top 5
            # In real AI system, use collaborative filtering or content-based filtering
            random.shuffle(available_books)
            recommendations = available_books[:5]

            return Response(
                {
                    "customer_id": customer_id,
                    "recommendations": recommendations,
                    "reason": "Personalized recommendations based on your preferences",
                }
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RecommendSimilarBooks(APIView):
    """
    Recommend books similar to a given book
    Based on category, author, or ratings
    """

    def get(self, request, book_id):
        try:
            # Get the target book
            book_response = requests.get(f"{BOOK_SERVICE_URL}/books/{book_id}/")
            if book_response.status_code != 200:
                return Response(
                    {"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND
                )

            target_book = book_response.json()

            # Get all books
            books_response = requests.get(f"{BOOK_SERVICE_URL}/books/")
            all_books = (
                books_response.json() if books_response.status_code == 200 else []
            )

            # Filter: same author or similar title (simple similarity)
            similar_books = []
            for book in all_books:
                if book["id"] == book_id:
                    continue
                # Simple matching: same author
                if book.get("author") == target_book.get("author"):
                    similar_books.append(book)

            # If not enough similar books, add random ones
            if len(similar_books) < 5:
                other_books = [
                    b
                    for b in all_books
                    if b["id"] != book_id and b not in similar_books
                ]
                random.shuffle(other_books)
                similar_books.extend(other_books[: 5 - len(similar_books)])

            return Response(
                {
                    "book_id": book_id,
                    "similar_books": similar_books[:5],
                    "reason": "Books you might also like",
                }
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PopularBooks(APIView):
    """Get most popular books based on ratings and sales"""

    def get(self, request):
        try:
            # Get all books
            books_response = requests.get(f"{BOOK_SERVICE_URL}/books/")
            all_books = (
                books_response.json() if books_response.status_code == 200 else []
            )

            # Get ratings for each book
            books_with_ratings = []
            for book in all_books:
                try:
                    rating_response = requests.get(
                        f"{COMMENT_RATE_SERVICE_URL}/reviews/book/{book['id']}/rating/"
                    )
                    if rating_response.status_code == 200:
                        rating_data = rating_response.json()
                        book["average_rating"] = rating_data.get("average_rating", 0)
                        book["total_reviews"] = rating_data.get("total_reviews", 0)
                    else:
                        book["average_rating"] = 0
                        book["total_reviews"] = 0
                except:
                    book["average_rating"] = 0
                    book["total_reviews"] = 0
                books_with_ratings.append(book)

            # Sort by rating and number of reviews
            books_with_ratings.sort(
                key=lambda x: (x["average_rating"], x["total_reviews"]), reverse=True
            )

            return Response(
                {
                    "popular_books": books_with_ratings[:10],
                    "reason": "Most popular books based on customer ratings",
                }
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TrendingBooks(APIView):
    """Get trending books (recently ordered)"""

    def get(self, request):
        try:
            # Get all books
            books_response = requests.get(f"{BOOK_SERVICE_URL}/books/")
            all_books = (
                books_response.json() if books_response.status_code == 200 else []
            )

            # Get recent orders
            try:
                orders_response = requests.get(f"{ORDER_SERVICE_URL}/orders/")
                orders = (
                    orders_response.json() if orders_response.status_code == 200 else []
                )
            except:
                orders = []

            # Count book occurrences in orders
            book_counts = {}
            for order in orders:
                items = order.get("items", [])
                for item in items:
                    book_id = item.get("book_id")
                    if book_id:
                        book_counts[book_id] = book_counts.get(book_id, 0) + 1

            # Sort books by order count
            for book in all_books:
                book["order_count"] = book_counts.get(book["id"], 0)

            all_books.sort(key=lambda x: x["order_count"], reverse=True)

            return Response(
                {
                    "trending_books": all_books[:10],
                    "reason": "Currently trending based on recent purchases",
                }
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
