#!/usr/bin/env python
"""
Script de validation de la configuration PWA
Vérifie que tous les fichiers et configurations PWA sont en place
"""

import os
import sys
import json
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
STATIC_DIR = PROJECT_DIR / 'eglise' / 'static'
ICONS_DIR = STATIC_DIR / 'icons'

def check_file_exists(path, description):
    """Vérifier si un fichier existe"""
    if path.exists():
        size = path.stat().st_size if path.is_file() else "dossier"
        print(f"  ✅ {description}: {path.name}")
        return True
    else:
        print(f"  ❌ {description}: MANQUANT - {path}")
        return False

def validate_manifest():
    """Valider le manifest.json"""
    print("\n📋 Vérification du Manifest...")
    manifest_path = STATIC_DIR / 'manifest.json'
    
    if not check_file_exists(manifest_path, "manifest.json"):
        return False
    
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        
        required_fields = ['name', 'short_name', 'start_url', 'display', 'icons']
        for field in required_fields:
            if field in manifest:
                print(f"    ✅ {field}: {manifest[field] if not isinstance(manifest[field], list) else f'({len(manifest[field])} items)'}")
            else:
                print(f"    ❌ {field}: MANQUANT")
                return False
        
        return True
    except Exception as e:
        print(f"  ❌ Erreur lors de la lecture du manifest: {e}")
        return False

def validate_scripts():
    """Valider les scripts JavaScript PWA"""
    print("\n📜 Vérification des Scripts...")
    
    scripts = [
        (STATIC_DIR / 'js' / 'service-worker.js', "Service Worker"),
        (STATIC_DIR / 'js' / 'pwa-init.js', "PWA Initialization"),
    ]
    
    all_ok = True
    for script_path, description in scripts:
        if not check_file_exists(script_path, description):
            all_ok = False
    
    return all_ok

def validate_templates():
    """Valider les templates"""
    print("\n🎨 Vérification des Templates...")
    
    templates = [
        (PROJECT_DIR / 'eglise' / 'templates' / 'eglise' / 'offline.html', "Page Offline"),
        (PROJECT_DIR / 'eglise' / 'templates' / 'eglise' / 'base.html', "Template de Base"),
    ]
    
    all_ok = True
    for template_path, description in templates:
        if not check_file_exists(template_path, description):
            all_ok = False
    
    # Vérifier que base.html contient les meta tags PWA
    if templates[1][0].exists():
        with open(templates[1][0], 'r', encoding='utf-8') as f:
            base_content = f.read()
            pwa_checks = [
                ('manifest.json', 'Manifest link'),
                ('mobile-web-app-capable', 'Mobile web app meta tag'),
                ('pwa-init.js', 'PWA init script'),
            ]
            for check_str, check_desc in pwa_checks:
                if check_str in base_content:
                    print(f"    ✅ {check_desc}")
                else:
                    print(f"    ❌ {check_desc}: MANQUANT")
                    all_ok = False
    
    return all_ok

def validate_icons():
    """Valider les icônes"""
    print("\n🎯 Vérification des Icônes...")
    
    if not ICONS_DIR.exists():
        print(f"  ❌ Répertoire des icônes: MANQUANT - {ICONS_DIR}")
        return False
    
    print(f"  ✅ Répertoire des icônes: {ICONS_DIR.name}")
    
    required_sizes = ['96x96', '192x192', '512x512']
    formats = ['png', 'svg', 'maskable.png', 'maskable.svg']
    
    all_ok = True
    for size in required_sizes:
        found = False
        for fmt in formats:
            icon_path = ICONS_DIR / f'icon-{size}.{fmt}' if fmt in ['png', 'svg'] else ICONS_DIR / f'icon-{size}-{fmt}'
            if icon_path.exists():
                print(f"    ✅ icon-{size}.{fmt}")
                found = True
        
        if not found:
            print(f"    ❌ icon-{size}: PAS DE VERSION TROUVÉE")
            all_ok = False
    
    # Vérifier les screenshots
    screenshots = ['screenshot-1.png', 'screenshot-2.png']
    for screenshot in screenshots:
        screenshot_path = ICONS_DIR / screenshot
        if screenshot_path.exists():
            print(f"    ✅ {screenshot}")
        else:
            print(f"    ❌ {screenshot}: MANQUANT")
            all_ok = False
    
    return all_ok

def validate_settings():
    """Valider les paramètres Django"""
    print("\n⚙️  Vérification de Settings.py...")
    
    settings_path = PROJECT_DIR / 'CCR' / 'settings.py'
    
    if not settings_path.exists():
        print(f"  ❌ settings.py: MANQUANT")
        return False
    
    with open(settings_path, 'r', encoding='utf-8') as f:
        settings_content = f.read()
    
    checks = [
        ('PWA_SERVICE_WORKER_PATH', 'PWA Configuration'),
        ('STATICFILES_STORAGE', 'Static files storage'),
        ('scheduler', 'Scheduler app'),
    ]
    
    all_ok = True
    for check_str, check_desc in checks:
        if check_str in settings_content:
            print(f"  ✅ {check_desc}")
        else:
            print(f"  ❌ {check_desc}: NON CONFIGURÉ")
            if check_str not in ['PWA_SERVICE_WORKER_PATH']:  # Non critique
                all_ok = False
    
    return all_ok

def validate_urls():
    """Valider les URLs"""
    print("\n🔗 Vérification des URLs...")
    
    urls_path = PROJECT_DIR / 'eglise' / 'urls.py'
    
    if not urls_path.exists():
        print(f"  ❌ urls.py: MANQUANT")
        return False
    
    with open(urls_path, 'r', encoding='utf-8') as f:
        urls_content = f.read()
    
    checks = [
        ('offline', 'Route offline'),
        ('ping', 'Route ping'),
    ]
    
    all_ok = True
    for check_str, check_desc in checks:
        if check_str in urls_content:
            print(f"  ✅ {check_desc}")
        else:
            print(f"  ❌ {check_desc}: NON TROUVÉE")
            all_ok = False
    
    return all_ok

def validate_views():
    """Valider les vues PWA"""
    print("\n👁️  Vérification des Vues...")
    
    views_path = PROJECT_DIR / 'eglise' / 'views.py'
    
    if not views_path.exists():
        print(f"  ❌ views.py: MANQUANT")
        return False
    
    with open(views_path, 'r', encoding='utf-8') as f:
        views_content = f.read()
    
    checks = [
        ('OfflineView', 'Vue Offline'),
        ('PingView', 'Vue Ping'),
    ]
    
    all_ok = True
    for check_str, check_desc in checks:
        if check_str in views_content:
            print(f"  ✅ {check_desc}")
        else:
            print(f"  ❌ {check_desc}: NON TROUVÉE")
            all_ok = False
    
    return all_ok

def main():
    """Exécuter toutes les validations"""
    print("=" * 60)
    print("🧪 VALIDATION DE LA CONFIGURATION PWA")
    print("=" * 60)
    
    results = {
        'Manifest': validate_manifest(),
        'Scripts': validate_scripts(),
        'Templates': validate_templates(),
        'Icons': validate_icons(),
        'Settings': validate_settings(),
        'URLs': validate_urls(),
        'Views': validate_views(),
    }
    
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DE LA VALIDATION")
    print("=" * 60)
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    for component, passed_check in results.items():
        status = "✅" if passed_check else "❌"
        print(f"{status} {component}")
    
    print("=" * 60)
    print(f"✅ Résultat: {passed}/{total} composants validés")
    
    if passed == total:
        print("\n🎉 EXCELLENT! Votre PWA est complètement configurée!")
        print("\n📝 Prochaines étapes:")
        print("   1. Démarrer le serveur: python manage.py runserver")
        print("   2. Ouvrir l'application dans le navigateur")
        print("   3. Installer la PWA depuis la barre d'adresse")
        print("   4. Tester le mode hors ligne")
        return 0
    else:
        print(f"\n⚠️  {total - passed} problème(s) détecté(s)")
        print("   Veuillez corriger les composants marqués en ❌")
        return 1

if __name__ == '__main__':
    sys.exit(main())
