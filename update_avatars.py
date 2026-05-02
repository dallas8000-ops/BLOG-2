from accounts.models import Profile

# Map usernames to avatar filenames
avatar_map = {
    'admin': 'admin.png',
    'cayden': 'cayden.png',
    'dallas8000': 'dallas8000.png',
    'kolton': 'kolton.png',
}

for username, avatar in avatar_map.items():
    try:
        profile = Profile.objects.get(user__username=username)
        profile.avatar = avatar
        profile.save()
        print(f"Updated {username} avatar to {avatar}")
    except Profile.DoesNotExist:
        print(f"Profile for {username} not found.")
