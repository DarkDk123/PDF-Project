#-----------IMPORT Statements-------------------
import PyPDF2 as pp
from pylovepdf.ilovepdf import ILovePdf

#--------CONSTANTS------------------------------
METADATA = {
    "/Author": "ENTERPRISE",
    "/Producer": "WEBSITE NAME",
    '/Title': 'TITLE'
}
PUBLIC_KEY = "project_public_45cd8ab370f8f81b6bf8b5d6c2abbfa0_qTqVO5c2601c6364553dfbb81909676f3fed4"

#--------Functions------------------------------------
def mergePDF(*files: (str)) -> None:
    """mergePDF is a func that takes Unlimited Positional Arguments(PDF File Paths),
    and merges them according to given order and outputs a file named "mergedfile.pdf" in the same directory."""
    try:
        merger = pp.PdfMerger()
        for f in files:
            merger.append(fileobj=f)

        merger.add_metadata(METADATA)
        merger.write(fileobj="./mergedfile.pdf")
        
    except FileNotFoundError as e:
        print("An ERROR Occured --> ", e, ": File_Not_Found_Error.")

    except pp.errors.PdfStreamError as e:
        print("An ERROR Occured --> ", e, ": Unable to Open PDF File.")

    except pp.errors.PdfReadError as e:
        print("An ERROR Occured --> ", e, ": A File is Encrypted.")

    finally:
        merger.close()


def compress(filepath: str) -> str:
    """
    Using Another Module pylovepdf that wraps
    Ilovepdf.com API For Efficient Compressing 
    of the PDF File and Returns folder path of compressed PDF
    """
    ilp = ILovePdf(public_key=PUBLIC_KEY)

    task = ilp.new_task(tool='compress')
    task.add_file(filepath)
    output_folder = "./compressed"
    task.set_output_folder(output_folder)
    task.execute()
    task.download()
    task.delete_current_task()
    return output_folder

    
def encryptPDF(filetoencrypt: str, password:str=None) -> None:
    reader = pp.PdfReader(filetoencrypt)
    writer = pp.PdfWriter()

    if reader.is_encrypted:
        print("Already Encrypted...")
        return
    # Add all pages to the writer
    for page in reader.pages:
        writer.add_page(page)

    # Add a password to the new PDF
    writer.encrypt(password)

    # Save the new PDF to a file
    with open("encrypted-pdf.pdf", "wb") as f:
        writer.write(f)

def unlockPDF(filetounlock: str, password:str):
    reader = pp.PdfReader(filetounlock)
    writer = pp.PdfWriter()

    if reader.is_encrypted:
        reader.decrypt(password=password)

    # Add all pages to the writer
    for page in reader.pages:
        writer.add_page(page)

    # Save the new PDF to a file
    with open("decrypted-pdf.pdf", "wb") as f:
        writer.write(f)

# Driver Code
if __name__ == "__main__":

    # mergePDF("C:/Users/VSMPRS/Documents/Zoom/darklord.pdf",
    #          "C:/Users/VSMPRS/Documents/Zoom\8,10.pdf")

    # reducesize(filetoreduce="C:/Users/VSMPRS/Documents/Zoom/8,10.pdf")
    encryptPDF("C:/Users/VSMPRS/Documents/Zoom/8,10.pdf")
