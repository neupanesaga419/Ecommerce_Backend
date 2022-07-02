from django.shortcuts import render
from reportlab.pdfgen import canvas
import io
from django.http import FileResponse
from reportlab.lib.pagesizes import letter
from NFSDATA.models import *
import pandas as pd
import os
from PIL import Image

# Create your views here.
def pdf_generator(request):
    
    # Create FileLike Buffer to recieve PDF data
    buffer = io.BytesIO()
        
    # Create the PDF object, using the buffer as its "file"
    p = canvas.Canvas(buffer,pagesize=letter)
    
    # Draw things on the PDF. Here's what the PDF generation Happens .
    # See the ReportLab Documentation for full list of functionality 
    p.drawString(-5, -5, "Welcome to PDF generation using Django")
    p.drawString(-100, -100, "Hello World")
    
    p.drawString(50, 10, "No one knows why")
    # p.drawPath("No Path")
    
    # Close the PDF object cleanly , and we're done
    p.showPage()
    p.save()
    
    # File response set the Content-Disposition header so that browsers present the option to save the file
    buffer.seek(0)
    
    return FileResponse(buffer,as_attachment=True,filename="hello.pdf")



def getPDF(request):
    
    buffer = io.BytesIO()
    
    p = canvas.Canvas(buffer,pagesize=letter)
    p.setLineWidth(.3)
    p.setFont('Helvetica', 12)
    p.drawString(30,750,'OFFICIAL COMMUNIQUE')
    p.drawString(30,735,'OF ACME INDUSTRIES')
    p.drawString(500,750,"12/12/2010")
    p.drawString(500,750,"12/12/2010")
    p.line(480,747,580,747)
    p.drawString(275,725,'AMOUNT OWED:')
    p.drawString(500,725,"$1,000.00")
    p.line(378,723,580,723)
    p.drawString(30,703,'RECEIVED BY:')
    p.line(120,700,580,700)
    p.drawString(120,703,"JOHN DOE")
    p.showPage()
    p.save()
    buffer.seek(0)
    # context["active_get_pdf"],context["bg_pdf"] = "active","bg-gradient-primary"
    return FileResponse(buffer,as_attachment=True,filename="letter.pdf")



def gen_pdf(request):
    
    buffer = io.BytesIO()
    # Creating Canvas
    c = canvas.Canvas(buffer,pagesize=(600,400),bottomup=0)

    # Logo Section
    # Setting th origin to (10,40)
    c.translate(60,110)
    # Inverting the scale for getting mirror Image of logo
    c.scale(1,-1)
    # Inserting Logo into the Canvas at required position
    # image = os.listdir("EditingTemplates/FileGenerators/logo.png")
    
    cwd = os.getcwd()
    img = "FileGenerators"
    
    image_path = os.path.join(cwd,img)
    img1 = "free.png"
    image_path = os.path.join(image_path,img1)
    print(image_path)
    c.drawImage(Image.open(image_path),0,0,width=100,height=100)
 
    # Title Section
    # Again Inverting Scale For strings insertion
    c.scale(1,-1)
    # Again Setting the origin back to (0,0) of top-left
    c.translate(-10,-40)
    # Setting the font for Name title of company
    c.setFont("Helvetica-Bold",15)
    # Inserting the name of the company
    c.drawCentredString(250,20,"Neupane Fancy Store")
    # For under lining the title
    c.line(150,22,230,22)
    # Changing the font size for Specifying Address
    c.setFont("Helvetica-Bold",5)
    c.drawCentredString(125,30,"Block No. 101, Triveni Apartments, Pitam Pura,")
    c.drawCentredString(125,35,"New Delhi - 110034, India")
    # Changing the font size for Specifying GST Number of firm
    c.setFont("Helvetica-Bold",6)
    c.drawCentredString(125,42,"GSTIN : 07AABCS1429B1Z")

    # Line Seprating the page header from the body
    c.line(5,45,195,45)

    # Document Information
    # Changing the font for Document title
    c.setFont("Courier-Bold",8)
    c.drawCentredString(100,55,"TAX-INVOICE")

    # This Block Consist of Costumer Details
    c.roundRect(15,63,170,40,10,stroke=1,fill=0)
    c.setFont("Times-Bold",5)
    c.drawRightString(70,70,"INVOICE No. :")
    c.drawRightString(70,80,"DATE :")
    c.drawRightString(70,90,"CUSTOMER NAME :")
    c.drawRightString(70,100,"PHONE No. :")

    # This Block Consist of Item Description
    c.roundRect(15,108,170,130,10,stroke=1,fill=0)
    c.line(15,120,185,120)
    c.drawCentredString(25,118,"SR No.")
    c.drawCentredString(75,118,"GOODS DESCRIPTION")
    c.drawCentredString(125,118,"RATE")
    c.drawCentredString(148,118,"QTY")
    c.drawCentredString(173,118,"TOTAL")
    # Drawing table for Item Description
    c.line(15,210,185,210)
    c.line(35,108,35,220)
    c.line(115,108,115,220)
    c.line(135,108,135,220)
    c.line(160,108,160,220)

    # Declaration and Signature
    c.line(15,220,185,220)
    c.line(100,220,100,238)
    c.drawString(20,225,"We declare that above mentioned")
    c.drawString(20,230,"information is true.")
    c.drawString(20,235,"(This is system generated invoive)")
    c.drawRightString(180,235,"Authorised Signatory")

    # End the Page and Start with new
    c.showPage()
    # Saving the PDF
    c.save()
    buffer.seek(0)
    return FileResponse(buffer,as_attachment=True,filename="pdfgen.pdf")







def gen_excel(request):
    
    our_data = Products.objects.all()
    
    collection = []
    print(len(our_data))
    
    for item in our_data:
        our_data_dict = {}
        our_data_dict["ID"] = item.id
        our_data_dict["Name"] = item.product_name
        our_data_dict["Quantity Present"] = item.product_amount
        our_data_dict["Cost Price"] = item.product_cost_price
        our_data_dict["Total Price"] = item.product_amount * item.product_cost_price
        
        collection.append(our_data_dict)
    
    total = 0
    total_item = 0
    for item in collection:
        for key,value in item.items():
            if key == "Total Price":
                total = total + item[key]
        for key,value in item.items():
            if key == "Quantity Present":
                total_item = total_item + item[key]
            
            
        
            
    # print(total)
    
    collection.append({"Name":"Total Items","Quantity Present":total_item,"Cost Price":"Grand Total","Total Price":total})
    # collection.append({"Total Price":total})
    # print(our_data_dict)   
        
    # collection = [
    #                 our_data_dict
    #                 ]
    output = io.BytesIO()
    
    df = pd.DataFrame(collection,columns=["ID","Name","Quantity Present","Cost Price","Total Price"])
    writer = pd.ExcelWriter(output,engine="xlsxwriter")
    df.to_excel(writer,sheet_name="Products Present")
    writer.save()
    output.seek(0)
    # response = StreamingHttpResponse(output,content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    return FileResponse(output,filename="spreadsheet.xlsx",as_attachment=True)
    