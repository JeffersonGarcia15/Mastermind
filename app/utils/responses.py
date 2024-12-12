# These are simply to avoid writing data: [], error: None | error every time. 
# I am following this approach because when I used supabase I saw that it followed that approach of const { data, error } = somethinghere

def error_response(message, status_code=400):
    return {"data": None, "error": message}, status_code

def success_response(data_obj, status_code=200):
    return {"data": data_obj, "error": None}, status_code
