from django.shortcuts import get_object_or_404, redirect, render
from models.auth_model import User


class UserController:
    @staticmethod
    def profile(request, user_id):
        profile = get_object_or_404(User, id=user_id)
        current_user_id = request.session.get('user_id')
        if request.method == 'POST' and current_user_id == profile.id:
            nome = request.POST.get('nome', '').strip()
            bio = request.POST.get('bio', '').strip()
            descricao = request.POST.get('descricao', '').strip()
            img = request.FILES.get('img')
            if nome:
                profile.nome = nome
            profile.bio = bio
            profile.descricao = descricao
            if img:
                profile.img = img
            try:
                profile.full_clean()
                profile.save()
            except Exception:
                return render(
                    request,
                    'user.html',
                    {
                        'profile': profile,
                        'current_user_id': current_user_id,
                        'error': 'Imagem inválida ou muito grande.',
                    },
                )
            if img:
                request.session['user_img'] = profile.img.url
            return redirect('user_profile', user_id=profile.id)
        return render(
            request,
            'user.html',
            {'profile': profile, 'current_user_id': current_user_id},
        )
