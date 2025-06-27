@echo off
:: This script creates the directory structure for the automated-blogging-engine.

echo Creating root directory...
mkdir automated-blogging-engine
cd automated-blogging-engine

echo Creating source directories...
mkdir src
mkdir src\config
mkdir src\agents
mkdir src\services
mkdir src\models
mkdir src\utils
mkdir src\templates

echo Creating test directories...
mkdir tests
mkdir tests\test_agents
mkdir tests\test_services
mkdir tests\test_utils

echo Creating data, logs, scripts, and docs directories...
mkdir data
mkdir logs
mkdir scripts
mkdir docs

echo Creating empty files...

:: Root files
type nul > .env.example
type nul > .gitignore
type nul > requirements.txt
type nul > pyproject.toml
type nul > README.md
type nul > Dockerfile

:: Src files
type nul > src\__init__.py
type nul > src\main.py
type nul > src\config\__init__.py
type nul > src\config\settings.py
type nul > src\config\categories.py
type nul > src\agents\__init__.py
type nul > src\agents\trend_spotter.py
type nul > src\agents\content_writer.py
type nul > src\agents\art_director.py
type nul > src\agents\publisher.py
type nul > src\services\__init__.py
type nul > src\services\gemini_client.py
type nul > src\services\image_service.py
type nul > src\services\github_service.py
type nul > src\services\seo_service.py
type nul > src\models\__init__.py
type nul > src\models\blog_post.py
type nul > src\models\category.py
type nul > src\models\api_response.py
type nul > src\utils\__init__.py
type nul > src\utils\file_handler.py
type nul > src\utils\markdown_processor.py
type nul > src\utils\topic_tracker.py
type nul > src\utils\validators.py
type nul > src\utils\logger.py
type nul > src\templates\blog_post_template.md
type nul > src\templates\frontmatter_template.py

:: Test files
type nul > tests\__init__.py
type nul > tests\test_agents\__init__.py
type nul > tests\test_agents\test_trend_spotter.py
type nul > tests\test_agents\test_content_writer.py
type nul > tests\test_agents\test_art_director.py
type nul > tests\test_services\__init__.py
type nul > tests\test_services\test_gemini_client.py
type nul > tests\test_services\test_image_service.py
type nul > tests\test_utils\__init__.py
type nul > tests\test_utils\test_file_handler.py
type nul > tests\test_utils\test_topic_tracker.py

:: Data files
type nul > data\used_topics.json
type nul > data\categories.json
type nul > data\generated_posts.json

:: Log files
type nul > logs\.gitkeep
type nul > logs\app.log
type nul > logs\errors.log

:: Script files
type nul > scripts\setup_environment.py
type nul > scripts\daily_generation.py
type nul > scripts\bulk_generate.py
type nul > scripts\cleanup_data.py

:: Doc files
type nul > docs\API.md
type nul > docs\CONFIGURATION.md
type nul > docs\DEPLOYMENT.md

echo.
echo Structure created successfully!
cd ..
pause