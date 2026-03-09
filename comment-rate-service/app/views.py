from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Review
from .serializers import ReviewSerializer
from django.db.models import Avg


@api_view(["GET"])
def api_index(request):
    """API Index - List all available endpoints"""
    return Response(
        {
            "service": "Comment & Rating Service",
            "version": "1.0",
            "description": "Customer can rate books",
            "endpoints": {
                "GET /reviews/": "List all reviews",
                "POST /reviews/": "Create review (customer rates book 1-5)",
                "GET /reviews/<id>/": "Get review details",
                "PUT /reviews/<id>/": "Update review",
                "DELETE /reviews/<id>/": "Delete review",
                "GET /reviews/book/<book_id>/": "Get all reviews for a book",
                "GET /reviews/book/<book_id>/rating/": "Get average rating for a book",
            },
        }
    )


class ReviewListCreate(APIView):
    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            # Check if customer already reviewed this book
            book_id = request.data.get("book_id")
            customer_id = request.data.get("customer_id")

            existing = Review.objects.filter(
                book_id=book_id, customer_id=customer_id
            ).first()
            if existing:
                # Update existing review
                existing.rating = request.data.get("rating", existing.rating)
                existing.comment = request.data.get("comment", existing.comment)
                existing.save()
                return Response(ReviewSerializer(existing).data)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewDetail(APIView):
    def get(self, request, pk):
        try:
            review = Review.objects.get(pk=pk)
            serializer = ReviewSerializer(review)
            return Response(serializer.data)
        except Review.DoesNotExist:
            return Response(
                {"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, pk):
        try:
            review = Review.objects.get(pk=pk)
            serializer = ReviewSerializer(review, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Review.DoesNotExist:
            return Response(
                {"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, pk):
        try:
            review = Review.objects.get(pk=pk)
            review.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Review.DoesNotExist:
            return Response(
                {"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND
            )


class BookReviews(APIView):
    """Get all reviews for a specific book"""

    def get(self, request, book_id):
        reviews = Review.objects.filter(book_id=book_id).order_by("-created_at")
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)


class BookAverageRating(APIView):
    """Get average rating for a specific book"""

    def get(self, request, book_id):
        reviews = Review.objects.filter(book_id=book_id)

        if not reviews.exists():
            return Response(
                {"book_id": book_id, "average_rating": 0, "total_reviews": 0}
            )

        avg_rating = reviews.aggregate(Avg("rating"))["rating__avg"]

        return Response(
            {
                "book_id": book_id,
                "average_rating": round(avg_rating, 2),
                "total_reviews": reviews.count(),
            }
        )
