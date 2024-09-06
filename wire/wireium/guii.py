import tkinter as tk
from tkinter import ttk
import webbrowser
import requests
from bs4 import BeautifulSoup
import wikipedia
from pytube import YouTube
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def search():
    try:
        keyword = entry.get()
        
        # Fetching Google search result
        url = f"https://www.google.com/search?q={keyword}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        result = soup.find('div', class_='BNeawe s3v9rd AP7Wnd')
        result_label.config(text=result.text if result else "No result found.")
        
        # Fetching Wikipedia summary
        try:
            wiki_summary = wikipedia.summary(keyword, sentences=2)
        except wikipedia.exceptions.DisambiguationError as e:
            wiki_summary = "Disambiguation Error: " + str(e)
        except wikipedia.exceptions.PageError:
            wiki_summary = "No Wikipedia page found."
        wiki_label.config(text=wiki_summary)
        
        # Fetching latest video from YouTube
        yt_url = f"https://www.youtube.com/results?search_query={keyword}"
        yt_response = requests.get(yt_url)
        yt_soup = BeautifulSoup(yt_response.text, 'html.parser')
        yt_link_tag = yt_soup.find('a', class_='yt-uix-tile-link')
        if yt_link_tag:
            yt_link = 'https://www.youtube.com' + yt_link_tag['href']
            yt_label.config(text=f"Latest Video: {yt_link}")
            # Download the first video
            yt_video = YouTube(yt_link)
            yt_stream = yt_video.streams.filter(progressive=True, file_extension='mp4').first()
            yt_stream.download()
        else:
            yt_label.config(text="No YouTube video found.")
    except Exception as e:
        result_label.config(text=f"Error: {str(e)}")
        wiki_label.config(text="")
        yt_label.config(text="")

def generate_pdf():
    try:
        keyword = entry.get()
        
        # Fetching Google search result
        url = f"https://www.google.com/search?q={keyword}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        result = soup.find('div', class_='BNeawe s3v9rd AP7Wnd')
        result_text = result.text if result else "No result found."

        # Fetching Wikipedia summary
        try:
            wiki_summary = wikipedia.summary(keyword, sentences=2)
        except wikipedia.exceptions.DisambiguationError as e:
            wiki_summary = "Disambiguation Error: " + str(e)
        except wikipedia.exceptions.PageError:
            wiki_summary = "No Wikipedia page found."
        
        # Fetching latest video from YouTube
        yt_url = f"https://www.youtube.com/results?search_query={keyword}"
        yt_response = requests.get(yt_url)
        yt_soup = BeautifulSoup(yt_response.text, 'html.parser')
        yt_link_tag = yt_soup.find('a', class_='yt-uix-tile-link')
        yt_link = 'https://www.youtube.com' + yt_link_tag['href'] if yt_link_tag else "No YouTube video found."
        
        # Create PDF document
        c = canvas.Canvas("article.pdf", pagesize=letter)
        c.setFont("Helvetica", 12)
        c.drawString(50, 750, f"Article: {keyword}")
        c.drawString(50, 730, f"Result: {result_text}")
        c.drawString(50, 710, f"Wikipedia Summary: {wiki_summary}")
        c.drawString(50, 690, f"Latest Video: {yt_link}")
        c.save()
        
        pdf_label.config(text="PDF generated successfully!")
    except Exception as e:
        pdf_label.config(text=f"Error: {str(e)}")

root = tk.Tk()
root.title("SEO Website Optimizer")

label = ttk.Label(root, text="Enter Keyword:")
label.pack()

entry = ttk.Entry(root)
entry.pack()

button = ttk.Button(root, text="Search", command=search)
button.pack()

result_label = ttk.Label(root, text="")
result_label.pack()

wiki_label = ttk.Label(root, text="")
wiki_label.pack()

yt_label = ttk.Label(root, text="")
yt_label.pack()

pdf_label = ttk.Label(root, text="")
pdf_label.pack()

generate_button = ttk.Button(root, text="Generate PDF", command=generate_pdf)
generate_button.pack()

root.mainloop()
