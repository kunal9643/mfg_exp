PROMPT = """

Input image is of the backside details of a product sold on e-commerce platform. 
You are an expert in identifying manufacturing date and expiry dates of the product given product description image.

Manufacturing date and Expiry dates can be found in different formats such as 

1. It can be in description shown by all three Day, Month and Year. 
2. It can be in description shown by Month and Year only, day can be missing.  
3. Only Manufacturing date is present and Expiry date is missing. But expiry date information is present implicitly, for example: Use before 6 months from the date of manufacturing. Then in this case, output expiry date should be calculated by adding the 6 months duration to the manufacturing date. Following is an example:
    
You have to output the Manufacturing date and Expiry date in DD/MM/YYYY format where D is day, M is month and Y is year If day is missing, return output in  MM/YYYY. 
    
In input image, Manufacturing date will always be written first. And then expiry date.
In some cases, dates are followed by special charactes like #, @ etc. For example: #02/24, @06/25, then return 02/24, 06/25 as output.

Also, return the number of months mentioned in the phrase starting from "Use Before". For example: If this is written Use before 30 Months from the date of manufacture, then return "30 months" as output as well in the json as "expiry duration". If not found then return null.  


Following are the example output jsons:
1.
{
    "Manufacturing Date": "10/08/2023",
    "Expiry Date": "10/10/2023",
    "Expiry Duration":"null",
}

2.
{
    "Manufacturing Date": "10/08/2023",
    "Expiry Date": "null",
    "Expiry Duration":"30 months",
}


"""
#Manufacturing date is denoted by 
#     - MFD
#     - PKD

# Expiry date is denoted by 
#     - Use by
#     - Exp
#     - Expiry date