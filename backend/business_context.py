from document_processor import (
    download_blob,
    extract_text_from_docx,
    extract_text_from_pdf,
    extract_data_from_csv,
    extract_data_from_excel,
)

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

import os


# ==========================================
# Azure Configuration
# ==========================================

load_dotenv()

STORAGE_ACCOUNT_URL = os.getenv("AZURE_STORAGE_ACCOUNT_URL")
CONTAINER_NAME = "synapse-documents"

credential = DefaultAzureCredential()

blob_service_client = BlobServiceClient(
    account_url=STORAGE_ACCOUNT_URL,
    credential=credential
)

container_client = blob_service_client.get_container_client(
    CONTAINER_NAME
)


# ==========================================
# List Files For One Business
# ==========================================

def list_uploaded_files(business_id: str):
    """
    Return only files belonging to the specified business.
    """

    prefix = f"{business_id}/"

    return [
        blob.name
        for blob in container_client.list_blobs(
            name_starts_with=prefix
        )
    ]


# ==========================================
# Read TXT / Markdown
# ==========================================

def read_text_file(filename: str):
    """
    Read TXT or Markdown files.
    """

    data = download_blob(filename)

    return data.decode("utf-8")


# ==========================================
# Summarize CSV
# ==========================================

def summarize_csv(filename: str):
    """
    Create a useful text summary of a CSV file.
    """

    df = extract_data_from_csv(filename)

    summary = []

    summary.append(f"FILE: {filename}")
    summary.append(f"Rows: {len(df)}")
    summary.append(f"Columns: {list(df.columns)}")

    summary.append("\nFIRST 10 ROWS:")

    summary.append(
        df.head(10).to_string(index=False)
    )

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns

    if len(numeric_columns) > 0:

        summary.append("\nNUMERIC SUMMARY:")

        summary.append(
            df[numeric_columns]
            .describe()
            .round(2)
            .to_string()
        )

    return "\n".join(summary)


# ==========================================
# Summarize Excel
# ==========================================

def summarize_excel(filename: str):
    """
    Create a useful text summary of an Excel file.
    """

    df = extract_data_from_excel(filename)

    summary = []

    summary.append(f"FILE: {filename}")
    summary.append(f"Rows: {len(df)}")
    summary.append(f"Columns: {list(df.columns)}")

    summary.append("\nFIRST 10 ROWS:")

    summary.append(
        df.head(10).to_string(index=False)
    )

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns

    if len(numeric_columns) > 0:

        summary.append("\nNUMERIC SUMMARY:")

        summary.append(
            df[numeric_columns]
            .describe()
            .round(2)
            .to_string()
        )

    return "\n".join(summary)


# ==========================================
# BUILD BUSINESS CONTEXT
# ==========================================

def build_business_context(business_id: str):
    """
    Build business context using ONLY files
    belonging to the specified business.
    """

    if not business_id:
        raise ValueError(
            "business_id is required to build business context."
        )

    files = list_uploaded_files(business_id)

    if not files:

        return (
            f"No business documents have been uploaded "
            f"for business_id: {business_id}"
        )

    context_parts = []

    context_parts.append(
        "BUSINESS INFORMATION FROM USER-UPLOADED FILES"
    )

    context_parts.append(
        f"BUSINESS ID: {business_id}"
    )

    context_parts.append(
        "The uploaded files are the source of truth."
    )

    context_parts.append(
        "Only files belonging to this business workspace "
        "are included in this context."
    )

    context_parts.append(
        "Do not assume a business type, company name, "
        "financial figures, dates, or products that are "
        "not present in the uploaded files."
    )

    # ==========================================
    # Process Only This Business's Files
    # ==========================================

    for filename in files:

        lower_name = filename.lower()

        try:

            if lower_name.endswith(".csv"):

                content = summarize_csv(filename)

            elif lower_name.endswith(
                (".xlsx", ".xls")
            ):

                content = summarize_excel(filename)

            elif lower_name.endswith(
                (".txt", ".md")
            ):

                content = read_text_file(filename)

            elif lower_name.endswith(".pdf"):

                content = extract_text_from_pdf(filename)

            elif lower_name.endswith(".docx"):

                content = extract_text_from_docx(filename)

            else:

                content = (
                    f"Unsupported file type: {filename}"
                )

            # Remove business_id/ from display name
            # so the agent sees the actual filename.
            display_name = filename

            prefix = f"{business_id}/"

            if display_name.startswith(prefix):
                display_name = display_name[len(prefix):]

            context_parts.append(
                f"\n===== {display_name} =====\n"
            )

            context_parts.append(content)

        except Exception as e:

            context_parts.append(
                f"\n===== {filename} =====\n"
                f"Could not process file: {str(e)}"
            )

    return "\n".join(context_parts)