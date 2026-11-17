"""
modules/routes.py
All Flask route definitions split into logical blueprints.
"""

import os
import json
from flask import (
    render_template_string, request, jsonify, redirect, url_for
)
from modules.database import (
    get_all_files, get_all_history, get_dashboard_stats,
    get_setting, set_setting
)
from modules.organizer import organize_file, preview_organization, get_folder_tree
from modules.classifier import get_all_categories, get_category_info, format_file_size
from modules.html_templates import (
    HOME_PAGE, ABOUT_PAGE, CONTACT_PAGE, DASHBOARD_PAGE,
    FILES_PAGE, HISTORY_PAGE, ORGANIZER_PAGE
)


def register_routes(app):
    """Register all application routes."""

    # ── Public pages ──────────────────────────────────────────────────────────

    @app.route("/")
    def home():
        stats = get_dashboard_stats(app.config["DATABASE"])
        return render_template_string(HOME_PAGE, stats=stats)

    @app.route("/about")
    def about():
        return render_template_string(ABOUT_PAGE)

    @app.route("/contact")
    def contact():
        return render_template_string(CONTACT_PAGE)

    # ── Dashboard ─────────────────────────────────────────────────────────────

    @app.route("/dashboard")
    def dashboard():
        stats = get_dashboard_stats(app.config["DATABASE"])
        size_fmt = format_file_size(stats["total_size_bytes"])
        cat_info = {c["category"]: get_category_info(c["category"])
                    for c in stats["categories"]}
        return render_template_string(
            DASHBOARD_PAGE, stats=stats, size_fmt=size_fmt, cat_info=cat_info
        )

    # ── File Organizer ────────────────────────────────────────────────────────

    @app.route("/organize", methods=["GET"])
    def organize_page():
        categories = get_all_categories()
        return render_template_string(ORGANIZER_PAGE, categories=categories)

    @app.route("/api/upload", methods=["POST"])
    def upload_files():
        if "files" not in request.files:
            return jsonify({"success": False, "message": "No files provided"}), 400

        files = request.files.getlist("files")
        results = []
        for f in files:
            if not f.filename:
                continue
            dest = os.path.join(app.config["UPLOAD_FOLDER"], f.filename)
            f.save(dest)
            result = organize_file(
                source_path=dest,
                organized_root=app.config["ORGANIZED_FOLDER"],
                db_path=app.config["DATABASE"],
                strategy="copy",
                duplicate=get_setting(app.config["DATABASE"],
                                      "duplicate_handling", "rename"),
            )
            result["filename"] = f.filename
            result["file_size_fmt"] = format_file_size(
                result.get("file_size", 0))
            results.append(result)

        organized = sum(1 for r in results if r.get("success"))
        return jsonify({
            "success": True,
            "total": len(results),
            "organized": organized,
            "results": results,
        })

    @app.route("/api/preview", methods=["POST"])
    def preview_files():
        data = request.get_json()
        filenames = data.get("filenames", [])
        preview = preview_organization(filenames)
        return jsonify({"preview": preview})

    @app.route("/api/folder-tree")
    def folder_tree():
        tree = get_folder_tree(app.config["ORGANIZED_FOLDER"])
        return jsonify(tree)

    # ── Files list ────────────────────────────────────────────────────────────

    @app.route("/files")
    def files_page():
        category = request.args.get("category", "")
        status = request.args.get("status", "")
        page = int(request.args.get("page", 1))
        per_page = 30
        offset = (page - 1) * per_page

        files = get_all_files(
            app.config["DATABASE"],
            limit=per_page,
            offset=offset,
            category=category or None,
            status=status or None,
        )
        for f in files:
            f["size_fmt"] = format_file_size(f.get("file_size", 0))
            info = get_category_info(f.get("category", "Others"))
            f["icon"] = info["icon"]
            f["color"] = info["color"]

        categories = get_all_categories()
        return render_template_string(
            FILES_PAGE, files=files, categories=categories,
            selected_cat=category, selected_status=status, page=page
        )

    # ── History ───────────────────────────────────────────────────────────────

    @app.route("/history")
    def history_page():
        history = get_all_history(app.config["DATABASE"])
        return render_template_string(HISTORY_PAGE, history=history)

    @app.route("/api/history")
    def history_api():
        history = get_all_history(app.config["DATABASE"], limit=500)
        return jsonify(history)

    # ── Settings API ──────────────────────────────────────────────────────────

    @app.route("/api/settings", methods=["GET"])
    def get_settings():
        keys = ["duplicate_handling", "organize_by", "auto_organize"]
        return jsonify({k: get_setting(app.config["DATABASE"], k) for k in keys})

    @app.route("/api/settings", methods=["POST"])
    def update_settings():
        data = request.get_json()
        for key, value in data.items():
            set_setting(app.config["DATABASE"], key, str(value))
        return jsonify({"success": True})

    # ── Stats API ─────────────────────────────────────────────────────────────

    @app.route("/api/stats")
    def stats_api():
        stats = get_dashboard_stats(app.config["DATABASE"])
        stats["total_size_fmt"] = format_file_size(stats["total_size_bytes"])
        return jsonify(stats)

    # ── Contact form ──────────────────────────────────────────────────────────

    @app.route("/api/contact", methods=["POST"])
    def contact_submit():
        data = request.get_json()
        # In production, send email; here we just acknowledge
        name = data.get("name", "")
        email = data.get("email", "")
        message = data.get("message", "")
        if not all([name, email, message]):
            return jsonify({"success": False, "message": "All fields required"}), 400
        return jsonify({
            "success": True,
            "message": f"Thanks {name}! We'll get back to you at {email}."
        })

    # ── 404 ───────────────────────────────────────────────────────────────────
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Not found"}), 404
