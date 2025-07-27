import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt

# ---------- Extract text from PDF ----------
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text

# ---------- Rank Resumes ----------
def rank_resumes(job_description, resume_texts, resume_names):
    documents = [job_description] + resume_texts
    tfidf = TfidfVectorizer().fit_transform(documents)
    vectors = tfidf.toarray()

    job_vec = vectors[0]
    resume_vecs = vectors[1:]
    scores = cosine_similarity([job_vec], resume_vecs).flatten()

    ranked = sorted(zip(resume_names, scores), key=lambda x: x[1], reverse=True)
    return ranked

# ---------- Upload Resumes and Rank ----------
def upload_and_rank():
    resume_paths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
    if not resume_paths:
        return

    # Get job description
    job_description = job_description_box.get("1.0", tk.END).strip()
    if not job_description:
        messagebox.showerror("Error", "Please enter a job description.")
        return

    resume_texts = []
    resume_names = []

    for path in resume_paths:
        text = extract_text_from_pdf(path)
        resume_texts.append(text)
        resume_names.append(os.path.basename(path))

    ranked = rank_resumes(job_description, resume_texts, resume_names)

    # Display results
    result_box.delete("1.0", tk.END)
    names = []
    scores = []

    for i, (name, score) in enumerate(ranked, 1):
        percent = round(score * 100, 2)
        result_box.insert(tk.END, f"{i}. {name} - Match Score: {percent}%\n")
        names.append(name)
        scores.append(percent)

    # Draw bar chart
    plt.figure(figsize=(8, 4))
    plt.barh(names[::-1], scores[::-1], color='skyblue')
    plt.xlabel("Match Percentage")
    plt.title("Resume Ranking")
    plt.tight_layout()
    plt.show()

# ---------- GUI Setup ----------
root = tk.Tk()
root.title("Simple Resume Ranker")
root.geometry("600x600")

# Job Description Input
tk.Label(root, text="Job Description:", font=('Arial', 12, 'bold')).pack(pady=5)
job_description_box = scrolledtext.ScrolledText(root, height=5, width=70)
job_description_box.pack(pady=5)

# Upload Button
upload_btn = tk.Button(root, text="📂 Upload Resumes and Rank", font=('Arial', 12), command=upload_and_rank)
upload_btn.pack(pady=10)

# Result Box
tk.Label(root, text="Ranking Results:", font=('Arial', 12, 'bold')).pack(pady=5)
result_box = scrolledtext.ScrolledText(root, height=10, width=70)
result_box.pack(pady=5)

# Run GUI
root.mainloop()
