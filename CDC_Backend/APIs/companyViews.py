import json
from datetime import datetime

from rest_framework.decorators import api_view

from .models import *
from .utils import *

logger = logging.getLogger('db')


@api_view(['POST'])
@precheck([COMPANY_NAME, ADDRESS, COMPANY_TYPE, NATURE_OF_BUSINESS, WEBSITE, COMPANY_DETAILS, IS_COMPANY_DETAILS_PDF,
           CONTACT_PERSON_NAME, PHONE_NUMBER, EMAIL, CITY, STATE, COUNTRY, PINCODE, DESIGNATION, DESCRIPTION,
           IS_DESCRIPTION_PDF,
           COMPENSATION_CTC, COMPENSATION_GROSS, COMPENSATION_TAKE_HOME, COMPENSATION_BONUS, COMPENSATION_DETAILS,
           IS_COMPENSATION_DETAILS_PDF,
           ALLOWED_BRANCH, SELECTION_PROCEDURE_ROUNDS, SELECTION_PROCEDURE_DETAILS, IS_SELECTION_PROCEDURE_DETAILS_PDF,
           TENTATIVE_DATE_OF_JOINING,
           TENTATIVE_NO_OF_OFFERS, OTHER_REQUIREMENTS
           ])
def addPlacement(request):
    try:
        data = request.data
        files = request.FILES
        opening = Placement()

        opening.id = generateRandomString()
        # Add a company details in the opening
        opening.company_name = data[COMPANY_NAME]
        opening.address = data[ADDRESS]
        opening.company_type = data[COMPANY_TYPE]
        opening.nature_of_business = data[NATURE_OF_BUSINESS]
        opening.website = data[WEBSITE]
        opening.company_details = data[COMPANY_DETAILS]
        if data[IS_COMPANY_DETAILS_PDF] == "true":
            opening.is_company_details_pdf = True
        elif data[IS_COMPANY_DETAILS_PDF] == "false":
            opening.is_company_details_pdf = False
        else:
            raise ValueError('Invalid value for is_company_details_pdf')

        if opening.is_company_details_pdf:
            company_details_pdf = []
            for file in files.getlist(COMPANY_DETAILS_PDF):
                file_location = STORAGE_DESTINATION_COMPANY_ATTACHMENTS + opening.id + '/'
                company_details_pdf.append(saveFile(file, file_location))

            opening.company_details_pdf_names = company_details_pdf

        # Add a contact person details in the opening
        opening.contact_person_name = data[CONTACT_PERSON_NAME]
        # Check if Phone number is Integer
        if data[PHONE_NUMBER].isdigit():
            opening.phone_number = int(data[PHONE_NUMBER])
        else:
            raise ValueError('Phone number should be integer')

        opening.email = data[EMAIL]

        # Add a company location in the opening
        opening.city = data[CITY]
        opening.state = data[STATE]
        opening.country = data[COUNTRY]

        # Check if Pincode is Integer
        if data[PINCODE].isdigit():
            opening.pin_code = int(data[PINCODE])
        else:
            raise ValueError('Pincode should be integer')

        # If India then set city_type as Domestic else International
        if opening.country == 'India':
            opening.city_type = 'Domestic'
        else:
            opening.city_type = 'International'

        # Add a designation details in the opening
        opening.designation = data[DESIGNATION]
        opening.description = data[DESCRIPTION]

        # Check if is_description_pdf is boolean
        if data[IS_DESCRIPTION_PDF] == "true":
            opening.is_description_pdf = True
        elif data[IS_DESCRIPTION_PDF] == "false":
            opening.is_description_pdf = False
        else:
            raise ValueError('Invalid value for is_description_pdf')

        if opening.is_description_pdf:
            description_pdf = []
            for file in files.getlist(DESCRIPTION_PDF):
                file_location = STORAGE_DESTINATION_COMPANY_ATTACHMENTS + opening.id + '/'
                description_pdf.append(saveFile(file, file_location))

            opening.description_pdf_names = description_pdf

        # Add a compensation details in the opening
        # Check if compensation_ctc is integer
        if data[COMPENSATION_CTC].isdigit():
            opening.compensation_CTC = int(data[COMPENSATION_CTC])
        elif data[COMPENSATION_CTC] is None:
            opening.compensation_CTC = None
        else:
            raise ValueError('Compensation CTC must be an integer')

        # Check if compensation_gross is integer
        if data[COMPENSATION_GROSS].isdigit():
            opening.compensation_gross = int(data[COMPENSATION_GROSS])
        elif data[COMPENSATION_GROSS] is None:
            opening.compensation_gross = None
        else:
            raise ValueError('Compensation Gross must be an integer')

        # Check if compensation_take_home is integer
        if data[COMPENSATION_TAKE_HOME].isdigit():
            opening.compensation_take_home = int(data[COMPENSATION_TAKE_HOME])
        elif data[COMPENSATION_TAKE_HOME] is None:
            opening.compensation_take_home = None
        else:
            raise ValueError('Compensation Take Home must be an integer')

        # Check if compensation_bonus is integer
        if data[COMPENSATION_BONUS].isdigit():
            opening.compensation_bonus = int(data[COMPENSATION_BONUS])
        elif data[COMPENSATION_BONUS] is None:
            opening.compensation_bonus = None
        else:
            raise ValueError('Compensation Bonus must be an integer')

        opening.compensation_details = data[COMPENSATION_DETAILS]
        # Check if is_compensation_details_pdf is boolean
        if data[IS_COMPENSATION_DETAILS_PDF] == "true":
            opening.is_compensation_details_pdf = True
        elif data[IS_COMPENSATION_DETAILS_PDF] == "false":
            opening.is_compensation_details_pdf = False
        else:
            raise ValueError('Invalid value for is_compensation_details_pdf')

        if opening.is_compensation_details_pdf:
            compensation_details_pdf = []
            for file in files.getlist(COMPENSATION_DETAILS_PDF):
                file_location = STORAGE_DESTINATION_COMPANY_ATTACHMENTS + opening.id + '/'
                compensation_details_pdf.append(saveFile(file, file_location))

            opening.compensation_details_pdf_names = compensation_details_pdf

        opening.bond_details = data[BOND_DETAILS]

        # Check if selection_procedure_rounds is list
        if data[SELECTION_PROCEDURE_ROUNDS] is None:
            raise ValueError('Selection Procedure Rounds cannot be empty')
        else:
            try:
                opening.selection_procedure_rounds = json.loads(data[SELECTION_PROCEDURE_ROUNDS])
            except:
                raise ValueError('Selection Procedure Rounds must be a list')
        opening.selection_procedure_details = data[SELECTION_PROCEDURE_DETAILS]
        # Check if is_selection_procedure_details_pdf is boolean
        if data[IS_SELECTION_PROCEDURE_DETAILS_PDF] == "true":
            opening.is_selection_procedure_details_pdf = True
        elif data[IS_SELECTION_PROCEDURE_DETAILS_PDF] == "false":
            opening.is_selection_procedure_details_pdf = False
        else:
            raise ValueError('Invalid value for is_selection_procedure_pdf')

        if opening.is_selection_procedure_details_pdf:
            selection_procedure_details_pdf = []
            for file in files.getlist(SELECTION_PROCEDURE_DETAILS_PDF):
                file_location = STORAGE_DESTINATION_COMPANY_ATTACHMENTS + opening.id + '/'
                selection_procedure_details_pdf.append(saveFile(file, file_location))

            opening.selection_procedure_details_pdf_names = selection_procedure_details_pdf

        stat, tier = getTier(opening.compensation_gross)
        if stat:
            opening.tier = tier
        else:
            raise ValueError('Invalid compensation gross')
        # Convert to date object
        opening.tentative_date_of_joining = datetime.strptime(data[TENTATIVE_DATE_OF_JOINING], '%d-%m-%Y').date()

        # Only Allowing Fourth Year for Placement
        opening.allowed_batch = [FOURTH_YEAR, ]
        # Check if allowed_branch are valid
        if data[ALLOWED_BRANCH] is None:
            raise ValueError('Allowed Branch cannot be empty')
        elif set(json.loads(data[ALLOWED_BRANCH])).issubset(BRANCHES):
            opening.allowed_branch = json.loads(data[ALLOWED_BRANCH])
        else:
            raise ValueError('Allowed Branch must be a subset of ' + str(BRANCHES))

        # Check if tentative_no_of_offers is integer
        if data[TENTATIVE_NO_OF_OFFERS].isdigit():
            opening.tentative_no_of_offers = int(data[TENTATIVE_NO_OF_OFFERS])
        else:
            raise ValueError('Tentative No Of Offers must be an integer')

        opening.other_requirements = data[OTHER_REQUIREMENTS]

        opening.save()

        data = {
            "designation": opening.designation,
            "opening_type": PLACEMENT,
            "opening_link": PLACEMENT_OPENING_URL.format(id=opening.id),  # Some Changes here too
            "company_name": opening.company_name
        }

        sendEmail(opening.email, COMPANY_OPENING_SUBMITTED_TEMPLATE_SUBJECT.format(id=opening.id), data,
                  COMPANY_OPENING_SUBMITTED_TEMPLATE)

        return Response({'action': "Add Placement", 'message': "Placement Added Successfully"},
                        status=status.HTTP_200_OK)

    except ValueError as e:
        return Response({'action': "Add Placement", 'message': str(e)},
                        status=status.HTTP_400_BAD_REQUEST)
    except:
        logger.warning("Add New Placement: " + str(sys.exc_info()))
        return Response({'action': "Add Placement", 'message': "Something went wrong"},
                        status=status.HTTP_400_BAD_REQUEST)
