from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from dara.mixins import AuthenticatedAPIView
from .models import PharmacyItem, Drug, PharmaCompany, Pharmacy


class PharmacyItemView(AuthenticatedAPIView):

    def get(self, request):
        pharmacy_id = request.GET.get('pharmacy_id')
        pharmacy_items = PharmacyItem.objects.filter(pharmacy_id=pharmacy_id)
        return Response({'pharmacy_items': pharmacy_items})
    
    def post(self, request):
        data = request.data
        drug_name = data.get('drug_name')
        count = data.get('count')
        company_id = data.get('company_id')
        pharmacy_id = data.get('pharmacy_id')
        explanation = data.get('explanation', '')
        expiration = data.get('expiration')
        locked = data.get('locked', 0)

        # Validate required fields
        if not all([drug_name, count, company_id, pharmacy_id, expiration]):
            return Response(
                {"error": "drug_name, count, company_id, pharmacy_id, and expiration are required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            with transaction.atomic():
                drug, created = Drug.objects.get_or_create(
                    name=drug_name,
                    pharma_company_id=company_id,
                    defaults={'explanation': explanation}
                )
                
                try:
                    pharmacy = Pharmacy.objects.get(id=pharmacy_id)
                except Pharmacy.DoesNotExist:
                    return Response(
                        {"error": "Pharmacy not found"}, 
                        status=status.HTTP_404_NOT_FOUND
                    )
                
                try:
                    pharma_company = PharmaCompany.objects.get(id=company_id)
                except PharmaCompany.DoesNotExist:
                    return Response(
                        {"error": "Pharma company not found"}, 
                        status=status.HTTP_404_NOT_FOUND
                    )
                
                # Create the pharmacy item
                pharmacy_item = PharmacyItem.objects.create(
                    drug=drug,
                    pharmacy=pharmacy,
                    pharma_company=pharma_company,
                    explanation=explanation,
                    expiration=expiration,
                    count=count,
                    locked=locked
                )
                
                return Response({
                    "success": True,
                    "pharmacy_item_id": pharmacy_item.id,
                    "message": "Pharmacy item created successfully"
                }, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            return Response(
                {"error": f"Failed to create pharmacy item: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def delete(self, request):
        data = request.data
        item_id = data.get('item_id')
        count = data.get('count')
        
        # Validate required fields
        if not all([item_id, count]):
            return Response(
                {"error": "item_id and count are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Find the pharmacy item
            pharmacy_item = PharmacyItem.objects.get(
                id=item_id
            )
            
            if not pharmacy_item:
                return Response(
                    {"error": "Pharmacy item not found"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            pharmacy_item.count = pharmacy_item.count - count
            pharmacy_item.save(update_fields=['count'])
            
            return Response({
                "success": True,
                "message": "Pharmacy item deleted successfully"
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {"error": f"Failed to delete pharmacy item: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



