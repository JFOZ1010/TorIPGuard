from django.http import JsonResponse

# Esta función la defino solo para ponerla en los endpoints como POST, PUT, DELETE, para solo los usuarios administradores== Super usuarios. 
def admin_required(view_func):
    # defino la funcion wrapped_view como privada para solo usarse dentro de permissions, y admin_required es el que se llama afuera. 
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            return JsonResponse({'error': 'Tu no tienes permiso para realizar esta acción :('}, status=403)
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# Con esta funcion lo que hago es basicamente validar que cualquier usuario pueda obtener los endpoints si está autenticado con el JWT, 
# como será usado como un decorador @user_permission_required solo lo pondré en los endpoints que sean de GET, ya que los de PUT, POST, DELETE, serán con @admin_required
def user_permission_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'La autenticación es requerida.'}, status=401)
        return view_func(request, *args, **kwargs)
    return _wrapped_view