#!/usr/bin/env python3
"""
Application Flask pour afficher et gérer les fichiers .mobi
"""

import os
from datetime import datetime
from flask import Flask, render_template, send_file, abort, redirect, url_for, request, flash
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['SECRET_KEY'] = 'votre-cle-secrete-ici'  # Nécessaire pour flash messages


def get_mobi_files():
    """
    Récupère la liste des fichiers .mobi dans le répertoire uploads
    triés par date de modification (plus récents en premier)
    
    Returns:
        list: Liste des dictionnaires contenant les infos des fichiers
    """
    upload_dir = app.config['UPLOAD_FOLDER']
    
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    files = []
    
    try:
        for filename in os.listdir(upload_dir):
            if filename.lower().endswith('.mobi'):
                file_path = os.path.join(upload_dir, filename)
                if os.path.isfile(file_path):
                    # Récupérer la date de modification
                    mod_time = os.path.getmtime(file_path)
                    mod_date = datetime.fromtimestamp(mod_time)
                    
                    # Récupérer la taille du fichier
                    file_size = os.path.getsize(file_path)
                    
                    files.append({
                        'filename': filename,
                        'modified': mod_date,
                        'size': file_size
                    })
        
        # Trier par date de modification (plus récents en premier)
        files.sort(key=lambda x: x['modified'], reverse=True)
        
    except OSError as e:
        print(f"Erreur lors de la lecture du répertoire: {e}")
    
    return files


@app.route('/')
def index():
    """
    Page principale affichant la liste des fichiers .mobi
    """
    files = get_mobi_files()
    return render_template('index.html', files=files)


@app.route('/download/<filename>')
def download_file(filename):
    """
    Route pour télécharger un fichier .mobi
    """
    # Sécuriser le nom du fichier
    safe_filename = secure_filename(filename)
    
    # Vérifier que le fichier se termine bien par .mobi
    if not safe_filename.lower().endswith('.mobi'):
        abort(400, "Fichier non autorisé")
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)
    
    # Vérifier que le fichier existe
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        abort(404, "Fichier non trouvé")
    
    try:
        return send_file(file_path, as_attachment=True, download_name=safe_filename)
    except Exception as e:
        print(f"Erreur lors du téléchargement: {e}")
        abort(500, "Erreur lors du téléchargement")


@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    """
    Route pour supprimer un fichier .mobi
    """
    # Sécuriser le nom du fichier
    safe_filename = secure_filename(filename)
    
    # Vérifier que le fichier se termine bien par .mobi
    if not safe_filename.lower().endswith('.mobi'):
        abort(400, "Fichier non autorisé")
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)
    
    # Vérifier que le fichier existe
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        abort(404, "Fichier non trouvé")
    
    try:
        os.remove(file_path)
        flash(f'Fichier "{safe_filename}" supprimé avec succès!', 'success')
        return redirect(url_for('index'))
    except OSError as e:
        print(f"Erreur lors de la suppression: {e}")
        abort(500, "Erreur lors de la suppression")


@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Route pour uploader un fichier .mobi
    """
    # Vérifier si un fichier a été envoyé
    if 'file' not in request.files:
        flash('Aucun fichier sélectionné', 'error')
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    # Vérifier si le fichier a un nom
    if file.filename == '':
        flash('Aucun fichier sélectionné', 'error')
        return redirect(url_for('index'))
    
    # Vérifier l'extension du fichier
    if not file.filename.lower().endswith('.mobi'):
        flash('Seuls les fichiers .mobi sont autorisés', 'error')
        return redirect(url_for('index'))
    
    # Sécuriser le nom du fichier
    filename = secure_filename(file.filename)
    
    # Vérifier que le fichier se termine bien par .mobi après sécurisation
    if not filename.lower().endswith('.mobi'):
        flash('Nom de fichier non valide', 'error')
        return redirect(url_for('index'))
    
    # Vérifier si le fichier existe déjà
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        flash(f'Le fichier "{filename}" existe déjà', 'error')
        return redirect(url_for('index'))
    
    try:
        # Sauvegarder le fichier
        file.save(file_path)
        flash(f'Fichier "{filename}" uploadé avec succès!', 'success')
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Erreur lors de l'upload: {e}")
        flash('Erreur lors de l\'upload du fichier', 'error')
        return redirect(url_for('index'))


@app.errorhandler(404)
def not_found(error):
    """Gestionnaire d'erreur 404"""
    return render_template('error.html', 
                         error_code=404, 
                         error_message="Page non trouvée"), 404


@app.errorhandler(500)
def internal_error(error):
    """Gestionnaire d'erreur 500"""
    return render_template('error.html', 
                         error_code=500, 
                         error_message="Erreur interne du serveur"), 500


@app.errorhandler(400)
def bad_request(error):
    """Gestionnaire d'erreur 400"""
    return render_template('error.html', 
                         error_code=400, 
                         error_message="Requête invalide"), 400


if __name__ == '__main__':
    # Créer le répertoire uploads s'il n'existe pas
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    # Démarrer le serveur Flask sur 0.0.0.0 pour accès externe
    app.run(host='0.0.0.0', port=5000, debug=True)
