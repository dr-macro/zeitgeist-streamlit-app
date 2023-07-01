mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
enableXsrfProtection=false\n\
\n\
\n\
[theme]\n\
primaryColor=\"#002171\"\n\
backgroundColor=\"#f3f4f6\"\n\
secondaryBackgroundColor=\"#FFFFFF\"\n\
textColor=\"#262730\"\n\
font=\"sans serif\"\n\
\n\
" > ~/.streamlit/config.toml
