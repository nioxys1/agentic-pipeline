import os
import time
import asyncio
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Chargement des variables
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GITLAB_TOKEN = os.getenv("GITLAB_TOKEN")
PROJECT_ID = os.getenv("GITLAB_PROJECT_ID")
GITLAB_URL = os.getenv("GITLAB_URL", "https://gitlab.com").rstrip('/')

HEADERS = {
    "PRIVATE-TOKEN": GITLAB_TOKEN
}

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = (
        "🤖 **Agent DevSecOps En Ligne**\n\n"
        "Je suis prêt à piloter votre pipeline GitLab sur la branche 'test'.\n"
        "Utilisez /help pour voir toutes les commandes disponibles."
    )
    await update.message.reply_text(welcome_message, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "**Commandes Disponibles :**\n\n"
        "🚀 `/run_pipeline` - Lancer l'intégration complète\n"
        "🔎 `/scan` - Lancer uniquement les outils de sécurité\n"
        "📦 `/deploy` - Lancer uniquement le déploiement\n"
        "📊 `/status` - Vérifier l'état du dernier pipeline\n"
        "📜 `/logs` - Afficher les logs du dernier job\n"
        "ℹ️ `/help` - Afficher ce menu d'aide"
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def run_pipeline_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Transmission de la commande à GitLab...")
    trigger_url = f"{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/pipeline?ref=test"
    
    try:
        response = requests.post(trigger_url, headers=HEADERS, timeout=10)
        if response.status_code == 201:
            data = response.json()
            msg = (
                "✅ **Pipeline complet démarré !**\n\n"
                f"🔹 **ID :** `{data.get('id')}`\n"
                f"🔗 [Suivre sur GitLab]({data.get('web_url')})"
            )
        else:
            msg = f"❌ Erreur GitLab : {response.text}"
    except Exception as e:
        msg = f"💥 Erreur réseau : {str(e)}"
    await update.message.reply_text(msg, parse_mode='Markdown', disable_web_page_preview=True)

async def scan_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔎 Démarrage exclusif des scans de sécurité via Tag...")
    
    # ASTUCE DEVSECOPS : On utilise un Tag pour contourner le blocage des variables
    tag_name = f"scan-{int(time.time())}"
    tag_url = f"{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/repository/tags"
    payload = {"tag_name": tag_name, "ref": "test"}
    
    try:
        response = requests.post(tag_url, headers=HEADERS, json=payload, timeout=10)
        if response.status_code == 201:
            await asyncio.sleep(2) # Laisse le temps à GitLab de générer le pipeline
            pipe_res = requests.get(f"{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/pipelines?ref={tag_name}", headers=HEADERS)
            if pipe_res.status_code == 200 and pipe_res.json():
                data = pipe_res.json()[0]
                msg = (
                    "✅ **Scan de sécurité lancé !**\n\n"
                    f"🔹 **ID :** `{data.get('id')}`\n"
                    f"🔗 [Suivre le scan]({data.get('web_url')})"
                )
            else:
                msg = "✅ **Scan lancé !** (Utilisez /status pour suivre)"
        else:
            msg = f"❌ Erreur GitLab : {response.text}"
    except Exception as e:
        msg = f"💥 Erreur réseau : {str(e)}"
    await update.message.reply_text(msg, parse_mode='Markdown', disable_web_page_preview=True)

async def deploy_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 Démarrage de la séquence de déploiement via Tag...")
    
    tag_name = f"deploy-{int(time.time())}"
    tag_url = f"{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/repository/tags"
    payload = {"tag_name": tag_name, "ref": "test"}
    
    try:
        response = requests.post(tag_url, headers=HEADERS, json=payload, timeout=10)
        if response.status_code == 201:
            await asyncio.sleep(2)
            pipe_res = requests.get(f"{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/pipelines?ref={tag_name}", headers=HEADERS)
            if pipe_res.status_code == 200 and pipe_res.json():
                data = pipe_res.json()[0]
                msg = (
                    "📦 **Déploiement en cours !**\n\n"
                    f"🔹 **ID :** `{data.get('id')}`\n"
                    f"🔗 [Suivre le déploiement]({data.get('web_url')})"
                )
            else:
                msg = "📦 **Déploiement lancé !** (Utilisez /status pour suivre)"
        else:
            msg = f"❌ Erreur GitLab : {response.text}"
    except Exception as e:
        msg = f"💥 Erreur réseau : {str(e)}"
    await update.message.reply_text(msg, parse_mode='Markdown', disable_web_page_preview=True)

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status_url = f"{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/pipelines?per_page=1"
    try:
        response = requests.get(status_url, headers=HEADERS, timeout=10)
        if response.status_code == 200 and response.json():
            latest_pipeline = response.json()[0]
            msg = (
                "📊 **État du dernier Pipeline :**\n\n"
                f"🔹 **ID :** `{latest_pipeline.get('id')}`\n"
                f"🔹 **Statut :** *{latest_pipeline.get('status').upper()}*\n"
                f"🔗 [Voir sur GitLab]({latest_pipeline.get('web_url')})"
            )
        else:
            msg = "⚠️ Aucun pipeline trouvé."
    except Exception as e:
        msg = f"💥 Erreur : {str(e)}"
    await update.message.reply_text(msg, parse_mode='Markdown', disable_web_page_preview=True)

async def logs_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 Récupération des logs du dernier job en cours...")
    pipeline_url = f"{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/pipelines?per_page=1"
    try:
        p_res = requests.get(pipeline_url, headers=HEADERS, timeout=10)
        if p_res.status_code == 200 and p_res.json():
            pipeline_id = p_res.json()[0]['id']
            jobs_url = f"{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/pipelines/{pipeline_id}/jobs"
            j_res = requests.get(jobs_url, headers=HEADERS, timeout=10)
            if j_res.status_code == 200 and j_res.json():
                last_job = j_res.json()[0]
                job_id = last_job['id']
                job_name = last_job['name']
                trace_url = f"{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/jobs/{job_id}/trace"
                t_res = requests.get(trace_url, headers=HEADERS, timeout=10)
                raw_logs = t_res.text
                tail_logs = raw_logs[-2000:] if len(raw_logs) > 2000 else raw_logs
                msg = f"📜 **Logs du job : `{job_name}`**\n```text\n{tail_logs}\n```"
            else:
                msg = "⚠️ Aucun job trouvé."
        else:
            msg = "⚠️ Aucun pipeline trouvé."
    except Exception as e:
        msg = f"💥 Erreur : {str(e)}"
    await update.message.reply_text(msg, parse_mode='Markdown')

if __name__ == '__main__':
    print("Démarrage de l'agent Telegram (Version avec Git Tags)...")
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('run_pipeline', run_pipeline_command))
    app.add_handler(CommandHandler('scan', scan_command))
    app.add_handler(CommandHandler('deploy', deploy_command))
    app.add_handler(CommandHandler('status', status_command))
    app.add_handler(CommandHandler('logs', logs_command))
    
    print("En attente de commandes (Appuyez sur Ctrl+C pour arrêter)...")
    app.run_polling(poll_interval=3)