import os

# Read the content of both files
with open('eglise/views.py', 'r', encoding='utf-8') as f:
    views_content = f.read()

with open('culte_views_addition.py', 'r', encoding='utf-8') as f:
    new_views_content = f.read()

# Append the new views to views.py, removing the comments at the top
new_views_to_add = '\n\n' + new_views_content.replace('# CULTE MANAGEMENT VIEWS - Add to eglise/views.py\n\n', '')

# Write the combined content back
with open('eglise/views.py', 'a', encoding='utf-8') as f:
    f.write(new_views_to_add)

print("✓ Added Culte views to eglise/views.py")

# Clean up
os.remove('culte_views_addition.py')
print("✓ Cleaned up temporary file")
