import os
from flask import Flask, request, redirect, url_for, send_from_directory, render_template_string, jsonify
import socket # Used to get the local IP address for display
from werkzeug.utils import secure_filename
from zeroconf import ServiceInfo, Zeroconf


# --- Configuration ---
# Determine the base directory of the script to ensure consistent paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define the folder where uploaded files will be stored
# Using os.path.join with BASE_DIR makes the path absolute and robust
UPLOAD_FOLDER = os.path.join(BASE_DIR, r'D:\uploads')

# ALLOWED_EXTENSIONS is removed to allow all file types as requested.
# Server will accept any file, but browser might still warn about unknown types.

# --- Flask Application Setup ---
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5000 * 1024 * 1024  # Max upload size: 50 MB

# --- Initialize UPLOAD_FOLDER and Example File ---
# Ensure the uploads directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
print(f"Server configured to use UPLOAD_FOLDER: {UPLOAD_FOLDER}")

# Create an example file if it doesn't exist, for initial testing
example_file_path = os.path.join(UPLOAD_FOLDER, 'example.txt')
if not os.path.exists(example_file_path):
    try:
        with open(example_file_path, 'w') as f:
            f.write('This is an example file.\n')
            f.write('You can upload, download, or delete files here.')
        print(f"Created example file: {example_file_path}")
    except IOError as e:
        print(f"Error creating example file {example_file_path}: {e}")

# --- HTML Template (Embedded directly in Python with embedded Tailwind CSS) ---
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en" class="dark"> <!-- Set to dark mode by default -->
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MK Cloud Server</title>
    <!-- Embedded Tailwind CSS for offline functionality -->
    <style>
        /* Compiled and Minified Tailwind CSS for the dark theme and responsive design */
        /*! tailwindcss v3.4.3 | MIT License | https://tailwindcss.com */
        /*
        This is a compiled version of the Tailwind CSS used in the previous design.
        It's embedded directly here to ensure the styling works without an internet connection.
        */
        *, ::before, ::after {
            box-sizing: border-box;
            border-width: 0;
            border-style: solid;
            border-color: #e5e7eb
        }
        ::before, ::after {
            --tw-content: ""
        }
        html {
            line-height: 1.5;
            -webkit-text-size-adjust: 100%;
            font-family: ui-sans-serif, system-ui, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
            font-feature-settings: normal;
            font-variation-settings: normal
        }
        body {
            margin: 0;
            line-height: inherit
        }
        hr {
            height: 0;
            color: inherit;
            border-top-width: 1px
        }
        abbr:where([title]) {
            text-decoration: underline dotted
        }
        h1, h2, h3, h4, h5, h6 {
            font-size: inherit;
            font-weight: inherit
        }
        a {
            color: inherit;
            text-decoration: inherit
        }
        b, strong {
            font-weight: bolder
        }
        code, kbd, samp, pre {
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
            font-size: 1em
        }
        small {
            font-size: 80%
        }
        sub, sup {
            font-size: 75%;
            line-height: 0;
            position: relative;
            vertical-align: baseline
        }
        sub {
            bottom: -0.25em
        }
        sup {
            top: -0.5em
        }
        table {
            text-indent: 0;
            border-color: inherit;
            border-collapse: collapse
        }
        button, input, optgroup, select, textarea {
            font-family: inherit;
            font-feature-settings: inherit;
            font-variation-settings: inherit;
            font-size: 100%;
            font-weight: inherit;
            line-height: inherit;
            color: inherit;
            margin: 0;
            padding: 0
        }
        button, select {
            text-transform: none
        }
        [type="button"], [type="reset"], [type="submit"] {
            -webkit-appearance: button;
            background-color: transparent;
            background-image: none
        }
        :-moz-focusring {
            outline: auto
        }
        :-moz-ui-invalid {
            box-shadow: none
        }
        progress {
            vertical-align: baseline
        }
        ::-webkit-inner-spin-button, ::-webkit-outer-spin-button {
            height: auto
        }
        [type="search"] {
            -webkit-appearance: textfield;
            outline-offset: -2px
        }
        ::-webkit-search-decoration {
            -webkit-appearance: none
        }
        ::-webkit-file-upload-button {
            -webkit-appearance: button;
            font: inherit
        }
        summary {
            display: list-item
        }
        blockquote, dl, dd, h1, h2, h3, h4, h5, h6, hr, figure, p, pre {
            margin: 0
        }
        fieldset {
            margin: 0;
            padding: 0
        }
        legend {
            padding: 0
        }
        ol, ul, menu {
            list-style: none;
            margin: 0;
            padding: 0
        }
        textarea {
            resize: vertical
        }
        input::placeholder, textarea::placeholder {
            opacity: 1;
            color: #9ca3af
        }
        button, [role="button"] {
            cursor: pointer
        }
        :disabled {
            cursor: default
        }
        img, svg, video, canvas, audio, iframe, embed, object {
            display: block;
            vertical-align: middle
        }
        img, video {
            max-width: 100%;
            height: auto
        }
        [hidden] {
            display: none
        }
        *, ::before, ::after {
            --tw-border-spacing-x: 0;
            --tw-border-spacing-y: 0;
            --tw-translate-x: 0;
            --tw-translate-y: 0;
            --tw-rotate: 0;
            --tw-skew-x: 0;
            --tw-skew-y: 0;
            --tw-scale-x: 1;
            --tw-scale-y: 1;
            --tw-pan-x: ;
            --tw-pan-y: ;
            --tw-pinch-zoom: ;
            --tw-scroll-snap-strictness: proximity;
            --tw-ordinal: ;
            --tw-slashed-zero: ;
            --tw-numeric-figure: ;
            --tw-numeric-spacing: ;
            --tw-numeric-fraction: ;
            --tw-ring-inset: ;
            --tw-ring-offset-width: 0px;
            --tw-ring-offset-color: #fff;
            --tw-ring-color: rgb(59 130 246 / .5);
            --tw-ring-offset-shadow: 0 0 #0000;
            --tw-ring-shadow: 0 0 #0000;
            --tw-shadow: 0 0 #0000;
            --tw-shadow-rgb: 0 0 0;
            --tw-filters: blur(0) saturate(1) brightness(1) contrast(1) grayscale(0) hue-rotate(0deg) invert(0) sepia(0) drop-shadow(0 0 #0000);
            --tw-backdrop-filters: blur(0) saturate(1) brightness(1) contrast(1) grayscale(0) hue-rotate(0deg) invert(0) sepia(0);
            --tw-contain-size: ;
            --tw-contain-layout: ;
            --tw-contain-paint: ;
            --tw-contain-style:
        }
        ::backdrop {
            --tw-border-spacing-x: 0;
            --tw-border-spacing-y: 0;
            --tw-translate-x: 0;
            --tw-translate-y: 0;
            --tw-rotate: 0;
            --tw-skew-x: 0;
            --tw-skew-y: 0;
            --tw-scale-x: 1;
            --tw-scale-y: 1;
            --tw-pan-x: ;
            --tw-pan-y: ;
            --tw-pinch-zoom: ;
            --tw-scroll-snap-strictness: proximity;
            --tw-ordinal: ;
            --tw-slashed-zero: ;
            --tw-numeric-figure: ;
            --tw-numeric-spacing: ;
            --tw-numeric-fraction: ;
            --tw-ring-inset: ;
            --tw-ring-offset-width: 0px;
            --tw-ring-offset-color: #fff;
            --tw-ring-color: rgb(59 130 246 / .5);
            --tw-ring-offset-shadow: 0 0 #0000;
            --tw-ring-shadow: 0 0 #0000;
            --tw-shadow: 0 0 #0000;
            --tw-shadow-rgb: 0 0 0;
            --tw-filters: blur(0) saturate(1) brightness(1) contrast(1) grayscale(0) hue-rotate(0deg) invert(0) sepia(0) drop-shadow(0 0 #0000);
            --tw-backdrop-filters: blur(0) saturate(1) brightness(1) contrast(1) grayscale(0) hue-rotate(0deg) invert(0) sepia(0);
            --tw-contain-size: ;
            --tw-contain-layout: ;
            --tw-contain-paint: ;
            --tw-contain-style:
        }
        .absolute {
            position: absolute
        }
        .relative {
            position: relative
        }
        .hidden {
            display: none
        }
        .flex {
            display: flex
        }
        .block {
            display: block
        }
        .w-full {
            width: 100%
        }
        .flex-grow {
            flex-grow: 1
        }
        .flex-col {
            flex-direction: column
        }
        .items-center {
            align-items: center
        }
        .items-start {
            align-items: flex-start
        }
        .justify-center {
            justify-content: center
        }
        .justify-between {
            justify-content: space-between
        }
        .justify-start {
            justify-content: flex-start
        }
        .space-x-2>:not([hidden])~:not([hidden]) {
            --tw-space-x: 0.5rem;
            margin-left: var(--tw-space-x);
            margin-right: 0
        }
        .space-y-3>:not([hidden])~:not([hidden]) {
            --tw-space-y: 0.75rem;
            margin-top: var(--tw-space-y);
            margin-bottom: 0
        }
        .space-y-4>:not([hidden])~:not([hidden]) {
            --tw-space-y: 1rem;
            margin-top: var(--tw-space-y);
            margin-bottom: 0
        }
        .space-y-8>:not([hidden])~:not([hidden]) {
            --tw-space-y: 2rem;
            margin-top: var(--tw-space-y);
            margin-bottom: 0
        }
        .rounded-full {
            border-radius: 9999px
        }
        .rounded-lg {
            border-radius: 0.5rem
        }
        .rounded-xl {
            border-radius: 0.75rem
        }
        .border {
            border-width: 1px
        }
        .border-2 {
            border-width: 2px
        }
        .border-dashed {
            border-style: dashed
        }
        .border-transparent {
            border-color: transparent
        }
        .border-gray-100 {
            border-color: #f3f4f6
        }
        .border-gray-200 {
            border-color: #e5e7eb
        }
        .border-gray-300 {
            border-color: #d1d5db
        }
        .border-red-400 {
            border-color: #f87171
        }
        .bg-white {
            background-color: #fff
        }
        .bg-gray-50 {
            background-color: #f9fafb
        }
        .bg-red-100 {
            background-color: #fee2e2
        }
        .bg-indigo-50 {
            background-color: #eef2ff
        }
        .bg-indigo-600 {
            background-color: #4f46e5
        }
        .bg-green-500 {
            background-color: #22c55e
        }
        .bg-red-500 {
            background-color: #ef4444
        }
        .p-2 {
            padding: 0.5rem
        }
        .p-4 {
            padding: 1rem
        }
        .p-6 {
            padding: 1.5rem
        }
        .p-8 {
            padding: 2rem
        }
        .px-4 {
            padding-left: 1rem;
            padding-right: 1rem
        }
        .py-2 {
            padding-top: 0.5rem;
            padding-bottom: 0.5rem
        }
        .py-3 {
            padding-top: 0.75rem;
            padding-bottom: 0.75rem
        }
        .py-4 {
            padding-top: 1rem;
            padding-bottom: 1rem
        }
        .py-12 {
            padding-top: 3rem;
            padding-bottom: 3rem
        }
        .px-6 {
            padding-left: 1.5rem;
            padding-right: 1.5rem
        }
        .mb-2 {
            margin-bottom: 0.5rem
        }
        .mb-4 {
            margin-bottom: 1rem
        }
        .mt-1 {
            margin-top: 0.25rem
        }
        .mt-4 {
            margin-top: 1rem
        }
        .mt-8 {
            margin-top: 2rem
        }
        .mr-4 {
            margin-right: 1rem
        }
        .text-center {
            text-align: center
        }
        .text-lg {
            font-size: 1.125rem;
            line-height: 1.75rem
        }
        .text-sm {
            font-size: 0.875rem;
            line-height: 1.25rem
        }
        .text-base {
            font-size: 1rem;
            line-height: 1.5rem
        }
        .text-2xl {
            font-size: 1.5rem;
            line-height: 2rem
        }
        .text-4xl {
            font-size: 2.25rem;
            line-height: 2.5rem
        }
        .font-semibold {
            font-weight: 600
        }
        .font-bold {
            font-weight: 700
        }
        .font-extrabold {
            font-weight: 800
        }
        .font-medium {
            font-weight: 500
        }
        .text-white {
            color: #fff
        }
        .text-gray-900 {
            color: #111827
        }
        .text-gray-600 {
            color: #4b5563
        }
        .text-gray-700 {
            color: #374151
        }
        .text-gray-500 {
            color: #6b7280
        }
        .text-red-700 {
            color: #b91c1c
        }
        .text-indigo-700 {
            color: #4338ca
        }
        .truncate {
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap
        }
        .shadow-sm {
            --tw-shadow: 0 1px 2px 0 rgb(0 0 0 / .05);
            --tw-shadow-rgb: 0 0 0;
            box-shadow: var(--tw-ring-offset-shadow, 0 0 #0000), var(--tw-ring-shadow, 0 0 #0000), var(--tw-shadow)
        }
        .shadow-lg {
            --tw-shadow: 0 10px 15px -3px rgb(0 0 0 / .1), 0 4px 6px -4px rgb(0 0 0 / .1);
            --tw-shadow-rgb: 0 0 0;
            box-shadow: var(--tw-ring-offset-shadow, 0 0 #0000), var(--tw-ring-shadow, 0 0 #0000), var(--tw-shadow)
        }
        .shadow-2xl {
            --tw-shadow: 0 25px 50px -12px rgb(0 0 0 / .25);
            --tw-shadow-rgb: 0 0 0;
            box-shadow: var(--tw-ring-offset-shadow, 0 0 #0000), var(--tw-ring-shadow, 0 0 #0000), var(--tw-shadow)
        }
        .shadow-inner {
            --tw-shadow: inset 0 2px 4px 0 rgb(0 0 0 / .05);
            --tw-shadow-rgb: 0 0 0;
            box-shadow: var(--tw-ring-offset-shadow, 0 0 #0000), var(--tw-ring-shadow, 0 0 #0000), var(--tw-shadow)
        }
        .focus\:outline-none:focus {
            outline: 2px solid transparent;
            outline-offset: 2px
        }
        .focus\:ring-2:focus {
            --tw-ring-offset-shadow: var(--tw-ring-inset) 0 0 0 var(--tw-ring-offset-width) var(--tw-ring-offset-color);
            --tw-ring-shadow: var(--tw-ring-inset) 0 0 0 calc(2px + var(--tw-ring-offset-width)) var(--tw-ring-color);
            box-shadow: var(--tw-ring-offset-shadow), var(--tw-ring-shadow), var(--tw-shadow, 0 0 #0000)
        }
        .focus\:ring-offset-2:focus {
            --tw-ring-offset-width: 2px
        }
        .focus\:ring-indigo-500:focus {
            --tw-ring-color: #6366f1
        }
        .hover\:border-indigo-500:hover {
            border-color: #6366f1
        }
        .hover\:bg-indigo-100:hover {
            background-color: #e0e7ff
        }
        .hover\:bg-indigo-700:hover {
            background-color: #4338ca
        }
        .hover\:bg-green-600:hover {
            background-color: #16a34a
        }
        .hover\:bg-red-600:hover {
            background-color: #dc2626
        }
        .transition {
            transition-property: color, background-color, border-color, text-decoration-color, fill, stroke, opacity, box-shadow, transform, filter, -webkit-backdrop-filter;
            transition-property: color, background-color, border-color, text-decoration-color, fill, stroke, opacity, box-shadow, transform, filter, backdrop-filter;
            transition-property: color, background-color, border-color, text-decoration-color, fill, stroke, opacity, box-shadow, transform, filter, backdrop-filter, -webkit-backdrop-filter;
            transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
            transition-duration: 0.15s
        }
        .ease-in-out {
            transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1)
        }
        .duration-150 {
            transition-duration: 0.15s
        }
        .duration-200 {
            transition-duration: 0.2s
        }
        .duration-300 {
            transition-duration: 0.3s
        }
        .min-h-screen {
            min-height: 100vh
        }
        .relative {
            position: relative
        }
        .absolute {
            position: absolute
        }
        .top-4 {
            top: 1rem
        }
        .right-4 {
            right: 1rem
        }
        .cursor-pointer {
            cursor: pointer
        }
        .bg-gradient-to-br {
            background-image: linear-gradient(to bottom right, var(--tw-gradient-stops))
        }
        .from-indigo-50 {
            --tw-gradient-from: #eef2ff;
            --tw-gradient-to: rgb(238 242 255 / 0)
        }
        .to-purple-100 {
            --tw-gradient-to: #ede9fe
        }
        .file\:mr-4::-webkit-file-upload-button {
            margin-right: 1rem
        }
        .file\:mr-4::file-selector-button {
            margin-right: 1rem
        }
        .file\:py-2::-webkit-file-upload-button {
            padding-top: 0.5rem;
            padding-bottom: 0.5rem
        }
        .file\:py-2::file-selector-button {
            padding-top: 0.5rem;
            padding-bottom: 0.5rem
        }
        .file\:px-4::-webkit-file-upload-button {
            padding-left: 1rem;
            padding-right: 1rem
        }
        .file\:px-4::file-selector-button {
            padding-left: 1rem;
            padding-right: 1rem
        }
        .file\:rounded-full::-webkit-file-upload-button {
            border-radius: 9999px
        }
        .file\:rounded-full::file-selector-button {
            border-radius: 9999px
        }
        .file\:border-0::-webkit-file-upload-button {
            border-width: 0
        }
        .file\:border-0::file-selector-button {
            border-width: 0
        }
        .file\:text-sm::-webkit-file-upload-button {
            font-size: 0.875rem;
            line-height: 1.25rem
        }
        .file\:text-sm::file-selector-button {
            font-size: 0.875rem;
            line-height: 1.25rem
        }
        .file\:font-semibold::-webkit-file-upload-button {
            font-weight: 600
        }
        .file\:font-semibold::file-selector-button {
            font-weight: 600
        }
        .file\:bg-indigo-50::-webkit-file-upload-button {
            background-color: #eef2ff
        }
        .file\:bg-indigo-50::file-selector-button {
            background-color: #eef2ff
        }
        .file\:text-indigo-700::-webkit-file-upload-button {
            color: #4338ca
        }
        .file\:text-indigo-700::file-selector-button {
            color: #4338ca
        }
        .hover\:file\:bg-indigo-100:hover::-webkit-file-upload-button {
            background-color: #e0e7ff
        }
        .hover\:file\:bg-indigo-100:hover::file-selector-button {
            background-color: #e0e7ff
        }
        @media (min-width: 640px) {
            .sm\:px-6 {
                padding-left: 1.5rem;
                padding-right: 1.5rem
            }
            .sm\:items-center {
                align-items: center
            }
            .sm\:mb-0 {
                margin-bottom: 0
            }
            .sm\:w-auto {
                width: auto
            }
        }
        @media (min-width: 1024px) {
            .lg\:px-8 {
                padding-left: 2rem;
                padding-right: 2rem
            }
        }

        /* Custom CSS from previous iterations, adjusted for dark mode defaults */
        body {
            font-family: 'Inter', sans-serif;
            transition: background-color 0.3s ease, color 0.3s ease;
            background-image: linear-gradient(to bottom right, #1a202c, #2d3748); /* Dark mode background */
        }
        .file-item, .drop-zone {
            transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out, background-color 0.3s ease;
        }
        .file-item:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        }
        .btn-primary, .btn-delete {
            transition: transform 0.15s ease-in-out, box-shadow 0.15s ease-in-out, background-color 0.3s ease;
        }
        .btn-primary:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .btn-delete:hover {
            background-color: #dc2626; /* Red-600 */
        }
        /* Dark mode specific styles - now applied by default */
        .bg-white { background-color: #2d3748; }
        .text-gray-900 { color: #e2e8f0; }
        .text-gray-600 { color: #a0aec0; }
        .bg-gray-50 { background-color: #4a5568; }
        .text-gray-800 { color: #e2e8f0; }
        .text-gray-700 { color: #cbd5e0; }
        .file-item { background-color: #4a5568; border-color: #2d3748; }
        .border-gray-200, .border-gray-100 { border-color: #4a5568; }
        .text-gray-500 { color: #a0aec0; }
        .file\:bg-indigo-50 { background-color: #4338ca; } /* Indigo-700 for dark mode */
        .file\:text-indigo-700 { color: #e0e7ff; } /* Indigo-100 for dark mode */
        .hover\:file\:bg-indigo-100:hover { background-color: #3730a3; } /* Indigo-800 for dark mode */
        .focus\:ring-indigo-500:focus { --tw-ring-color: #6366f1; } /* Indigo-500 for dark mode */
        .bg-indigo-600 { background-color: #4f46e5; }
        .hover\:bg-indigo-700:hover { background-color: #4338ca; }
        .bg-green-500 { background-color: #22c55e; }
        .hover\:bg-green-600:hover { background-color: #16a34a; }
        .bg-red-500 { background-color: #ef4444; }
        .hover\:bg-red-600:hover { background-color: #dc2626; }
        .drop-zone.highlight { border-color: #818cf8; background-color: rgba(129, 140, 248, 0.1); }

        /* Mobile-friendly adjustments (apply to all screen sizes for mobile-first) */
        .max-w-4xl {
            max-width: 100%;
            padding: 1rem;
        }
        @media (min-width: 640px) {
            .max-w-4xl {
                max-width: 56rem;
                padding: 2rem;
            }
        }
        .file-item {
            flex-direction: column;
            align-items: flex-start;
        }
        .file-item .flex.space-x-2 {
            width: 100%;
            justify-content: flex-start;
            margin-top: 0.5rem;
        }
    </style>
</head>
<body class="min-h-screen flex flex-col items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-4xl w-full bg-white p-8 rounded-xl shadow-2xl space-y-8 border border-gray-200">
        <div class="text-center">
            <h1 class="text-4xl font-extrabold text-gray-900 mb-4">
                MK Cloud Server
            </h1>
            <p class="text-lg text-gray-600">
                Upload and download files seamlessly across your network.
            </p>
        </div>

        <!-- Error Message Display -->
        <div id="error-message" class="hidden bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
            <strong class="font-bold">Error!</strong>
            <span class="block" id="error-text"></span>
        </div>

        <!-- Upload Section -->
        <div class="bg-gray-50 p-6 rounded-lg shadow-inner border border-gray-100">
            <h2 class="text-2xl font-semibold text-gray-800 mb-4">Upload a File</h2>
            
            <!-- Drag and Drop Zone -->
            <div id="drop-zone" class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center cursor-pointer hover:border-indigo-500">
                <p class="text-gray-600 text-lg">Drag & Drop files here, or click to browse</p>
                <p class="text-sm text-gray-500 mt-1">Max file size: 5GB. All file types are allowed.</p>
                <input type="file" id="hidden-file-input" name="file" multiple class="hidden">
            </div>

            <!-- Traditional Upload Form (hidden, but can be shown if needed) -->
            <form id="upload-form" action="/" method="post" enctype="multipart/form-data" class="mt-4 space-y-4 hidden">
                <label for="file-upload" class="block text-sm font-medium text-gray-700">
                    Select your file:
                </label>
                <div class="flex items-center space-x-3">
                    <input id="file-upload" name="file" type="file" class="block w-full text-sm text-gray-900
                        file:mr-4 file:py-2 file:px-4
                        file:rounded-full file:border-0
                        file:text-sm file:font-semibold
                        file:bg-indigo-50 file:text-indigo-700
                        hover:file:bg-indigo-100
                        cursor-pointer focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2" />
                    <button type="submit" class="btn-primary inline-flex items-center px-6 py-2 border border-transparent text-base font-medium rounded-full shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition ease-in-out duration-150">
                        Upload
                    </button>
                </div>
            </form>
        </div>

        <!-- Download Section -->
        <div class="bg-white p-6 rounded-lg shadow-lg border border-gray-100">
            <h2 class="text-2xl font-semibold text-gray-800 mb-4">Available Files</h2>
            <ul id="file-list" class="space-y-3">
                <!-- Files will be loaded here by JavaScript -->
                <p class="text-gray-600 text-center py-4">Loading files...</p>
            </ul>
        </div>

        <p class="text-center text-sm text-gray-500 mt-8">
            <span class="font-semibold">Note:</span> This server is accessible to all devices on the same Wi-Fi network. Find your server's IP address 192.168.1.4 and port `5000` to access it from other devices.
        </p>
    </div>

    <script>
        const dropZone = document.getElementById('drop-zone');
        const hiddenFileInput = document.getElementById('hidden-file-input');
        const errorMessageDiv = document.getElementById('error-message');
        const errorTextSpan = document.getElementById('error-text');
        const fileListUl = document.getElementById('file-list');

        function showErrorMessage(message) {
            errorTextSpan.textContent = message;
            errorMessageDiv.classList.remove('hidden');
            setTimeout(() => {
                errorMessageDiv.classList.add('hidden');
            }, 5000); // Hide after 5 seconds
        }

        dropZone.addEventListener('click', () => {
            hiddenFileInput.click(); // Trigger hidden file input click
        });

        hiddenFileInput.addEventListener('change', (event) => {
            const files = event.target.files;
            handleFiles(files);
        });

        dropZone.addEventListener('dragover', (event) => {
            event.preventDefault();
            dropZone.classList.add('highlight');
        });

        dropZone.addEventListener('dragleave', (event) => {
            dropZone.classList.remove('highlight');
        });

        dropZone.addEventListener('drop', (event) => {
            event.preventDefault();
            dropZone.classList.remove('highlight');
            const files = event.dataTransfer.files;
            handleFiles(files);
        });

        function handleFiles(files) {
            if (files.length === 0) {
                return;
            }

            const formData = new FormData();
            for (let i = 0; i < files.length; i++) {
                const file = files[i];
                formData.append('file', file); // Append all files directly
            }
            
            // Submit the form data
            fetch('/', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                // Flask redirects on success or error, so let the browser handle it.
                // The page reload will trigger fetchFiles() on DOMContentLoaded.
                if (response.redirected) {
                    window.location.href = response.url;
                } else {
                    response.text().then(text => {
                        console.error('Server response:', text);
                        showErrorMessage('Upload failed: ' + (text || 'Unknown error.'));
                    });
                }
            })
            .catch(error => {
                console.error('Upload failed:', error);
                showErrorMessage('Network error during upload.');
            });
        }

        // Function to update the file list dynamically
        function updateFileList(files) {
            let filesHtml = '';
            if (files.length > 0) {
                files.forEach(file => {
                    filesHtml += `
                    <li class="file-item flex flex-col items-start justify-between p-4 bg-gray-50 rounded-lg shadow-sm transition ease-in-out duration-200 border border-gray-100">
                        <span class="text-lg text-gray-800 font-medium truncate flex-grow mr-4 mb-2">${file}</span>
                        <div class="flex space-x-2 w-full justify-start">
                            <a href="/download/${file}" class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-full shadow-sm text-white bg-green-500 hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition ease-in-out duration-150">
                                Download
                            </a>
                            <form action="/delete/${file}" method="post" onsubmit="return confirm('Are you sure you want to delete ${file}?');">
                                <button type="submit" class="btn-delete inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-full shadow-sm text-white bg-red-500 hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition ease-in-out duration-150">
                                    Delete
                                </button>
                            </form>
                        </div>
                    </li>
                    `;
                });
            } else {
                filesHtml = '<p class="text-gray-600 text-center py-4">No files uploaded yet. Be the first to share!</p>';
            }
            fileListUl.innerHTML = filesHtml;

            // Re-attach confirm handlers for newly added forms
            fileListUl.querySelectorAll('form').forEach(form => {
                form.onsubmit = function() {
                    // Extract filename from the preceding span for the confirmation message
                    const fileNameSpan = form.closest('li').querySelector('span');
                    const fileName = fileNameSpan ? fileNameSpan.textContent.trim() : 'this file';
                    return confirm(`Are you sure you want to delete ${fileName}?`);
                };
            });
        }

        // Function to fetch files from the server via JSON endpoint
        function fetchFiles() {
            fetch('/files_json')
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        console.error('Error fetching files:', data.error);
                        showErrorMessage('Could not load file list.');
                    } else {
                        updateFileList(data);
                    }
                })
                .catch(error => {
                    console.error('Network error fetching files:', error);
                    showErrorMessage('Network error loading file list.');
                });
        }

        // Initial load and periodic refresh of file list
        document.addEventListener('DOMContentLoaded', () => {
            fetchFiles(); // Load files on page load
            setInterval(fetchFiles, 2000); // Refresh every 2 seconds
        });

        // Check for server-side error message in URL query parameters
        const urlParams = new URLSearchParams(window.location.search);
        const serverErrorMessage = urlParams.get('error');
        if (serverErrorMessage) {
            showErrorMessage(serverErrorMessage);
            // Optionally clear the error from URL after displaying
            // history.replaceState(null, '', window.location.pathname);
        }
    </script>
</body>
</html>
'''

# --- Flask Routes ---
@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Handles both displaying the main page and processing file uploads.
    """
    error_message = request.args.get('error') # Get error message from query parameter

    if request.method == 'POST':
        # Check if a file was submitted in the form
        if 'file' not in request.files:
            print("Upload Warning: No 'file' part in the request.")
            return redirect(url_for('index', error="No file selected for upload."))

        uploaded_file = request.files['file']

        # If the user submits an empty file input
        if uploaded_file.filename == '':
            print("Upload Warning: No selected file (empty filename).")
            return redirect(url_for('index', error="No file selected for upload."))

        # Since all file types are allowed, no 'allowed_file' check is needed.
        # Max file size is still enforced by app.config['MAX_CONTENT_LENGTH']
        filename = secure_filename(uploaded_file.filename)
        file_save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            uploaded_file.save(file_save_path)
            print(f"File '{filename}' uploaded successfully to: {file_save_path}")
        except IOError as e:
            print(f"IOError saving file '{filename}' to '{file_save_path}': {e}")
            return redirect(url_for('index', error=f"Server error: Permissions issue saving '{filename}'."))
        except Exception as e:
            print(f"General Error saving file '{filename}' to '{file_save_path}': {e}")
            return redirect(url_for('index', error=f"Server error saving '{filename}': {e}"))
        return redirect(url_for('index'))

    # For GET requests, list files and render the page
    # The initial file list is empty, as JS will fetch it dynamically
    return render_template_string(HTML_TEMPLATE, files=[], error_message=error_message)

@app.route('/files_json')
def files_json():
    """
    Returns a JSON list of files in the UPLOAD_FOLDER.
    Used by JavaScript for real-time updates.
    """
    files = []
    try:
        if os.path.exists(app.config['UPLOAD_FOLDER']):
            files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], f))]
            files.sort()
        return jsonify(files)
    except Exception as e:
        print(f"Error fetching files for JSON: {e}")
        return jsonify({"error": "Could not retrieve files"}), 500


@app.route('/download/<path:filename>')
def download_file(filename):
    """
    Allows users to download files from the UPLOAD_FOLDER.
    Uses send_from_directory for secure and robust file serving.
    The <path:filename> converter allows filenames with slashes (though secure_filename sanitizes them).
    """
    print(f"--- Download Request Debug ---")
    print(f"Request URL: {request.url}")
    print(f"Raw filename from URL parameter: {filename}")

    secured_filename = secure_filename(filename)
    print(f"Secured filename for download: {secured_filename}")

    # Construct the full absolute path to the file
    full_file_path = os.path.join(app.config['UPLOAD_FOLDER'], secured_filename)
    print(f"Constructed full file path for download: {full_file_path}")

    # Check if the file actually exists at the constructed path
    if not os.path.exists(full_file_path):
        print(f"Download Error: File '{secured_filename}' not found at '{full_file_path}'. Sending 404.")
        return "File not found.", 404
    
    try:
        # Serve the file from the configured UPLOAD_FOLDER
        # as_attachment=True prompts the browser to download instead of display
        print(f"Attempting send_from_directory for directory: {app.config['UPLOAD_FOLDER']}, filename: {secured_filename}")
        return send_from_directory(app.config['UPLOAD_FOLDER'], secured_filename, as_attachment=True)
    except FileNotFoundError:
        # This catch is mostly for robustness, as os.path.exists should ideally catch it
        print(f"Download Error: File '{secured_filename}' not found during send_from_directory (caught by FileNotFoundError).")
        return "File not found (internal error).", 404
    except Exception as e:
        print(f"General Download Error for '{secured_filename}': {e}")
        return "An error occurred during download.", 500
    print(f"--- End Download Request Debug ---")


@app.route('/delete/<path:filename>', methods=['POST'])
def delete_file(filename):
    """
    Allows users to delete files from the UPLOAD_FOLDER.
    """
    secured_filename = secure_filename(filename)
    full_path = os.path.join(app.config['UPLOAD_FOLDER'], secured_filename)
    print(f"Attempting to delete file: {full_path}")

    if os.path.isfile(full_path):
        try:
            os.remove(full_path)
            print(f"File '{secured_filename}' deleted successfully from: {full_path}")
        except Exception as e:
            print(f"Error deleting file '{secured_filename}' from '{full_path}': {e}")
    else:
        print(f"Delete Error: File '{secured_filename}' not found at '{full_path}' for deletion.")
    return redirect(url_for('index'))

# --- Server Run ---
def register_mdns(name="mycloud", port=5000):
    zeroconf = Zeroconf()
    
    # Get IP as bytes
    ip_str = socket.gethostbyname(socket.gethostname())
    ip_bytes = socket.inet_aton(ip_str)

    # Create service info
    service_info = ServiceInfo(
        type_="_http._tcp.local.",
        name=f"{name}._http._tcp.local.",
        addresses=[ip_bytes],  # <- fixed here
        port=port,
        properties={},
        server=f"{name}.local."
    )
    
    zeroconf.register_service(service_info)
    print(f"mDNS service registered at: http://{name}.local:{port}")
    return zeroconf

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))