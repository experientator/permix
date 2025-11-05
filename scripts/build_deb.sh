#!/bin/bash

# Настройки пакета
APP_NAME="permix"
VERSION="0.2.4"
ARCHITECTURE="all"
MAINTAINER="Schmidberskaya & Simonenko <shap.20@uni-dubna.ru>"

echo "=== Building DEB package for $APP_NAME ==="

BUILD_DIR="$HOME/permix_build"
rm -rf $BUILD_DIR
mkdir -p $BUILD_DIR/DEBIAN
mkdir -p $BUILD_DIR/usr/bin
mkdir -p $BUILD_DIR/usr/lib/$APP_NAME
mkdir -p $BUILD_DIR/usr/share/applications
mkdir -p $BUILD_DIR/usr/share/icons/hicolor/256x256/apps
mkdir -p $BUILD_DIR/usr/share/doc/$APP_NAME

echo "Copying application files..."
WINDOWS_PROJECT_PATH="/mnt/c/Users/арина!/PycharmProjects/permix_remake"

cp "$WINDOWS_PROJECT_PATH/main.py" $BUILD_DIR/usr/lib/$APP_NAME/
cp "$WINDOWS_PROJECT_PATH/data.db" $BUILD_DIR/usr/lib/$APP_NAME/
cp "$WINDOWS_PROJECT_PATH/requirements.txt" $BUILD_DIR/usr/lib/$APP_NAME/
cp "$WINDOWS_PROJECT_PATH/README.md" $BUILD_DIR/usr/lib/$APP_NAME/ 2>/dev/null || true

# Копируем ВСЮ структуру src директории
if [ -d "$WINDOWS_PROJECT_PATH/src" ]; then
    mkdir -p $BUILD_DIR/usr/lib/$APP_NAME/src
    cp -r "$WINDOWS_PROJECT_PATH/src"/* $BUILD_DIR/usr/lib/$APP_NAME/src/ 2>/dev/null || true
fi

# Копируем summary директорию
if [ -d "$WINDOWS_PROJECT_PATH/summary" ]; then
    cp -r "$WINDOWS_PROJECT_PATH/summary" $BUILD_DIR/usr/lib/$APP_NAME/
fi

# Копируем tests директорию
if [ -d "$WINDOWS_PROJECT_PATH/tests" ]; then
    mkdir -p $BUILD_DIR/usr/lib/$APP_NAME/tests
    cp -r "$WINDOWS_PROJECT_PATH/tests"/* $BUILD_DIR/usr/lib/$APP_NAME/tests/ 2>/dev/null || true
fi

# Если есть иконка
if [ -f "$WINDOWS_PROJECT_PATH/icon.ico" ]; then
    cp "$WINDOWS_PROJECT_PATH/icon.ico" $BUILD_DIR/usr/share/icons/hicolor/256x256/apps/$APP_NAME.png
elif [ -f "$WINDOWS_PROJECT_PATH/icon.png" ]; then
    cp "$WINDOWS_PROJECT_PATH/icon.png" $BUILD_DIR/usr/share/icons/hicolor/256x256/apps/$APP_NAME.png
fi

# Создаем __init__.py файлы для правильной работы импортов
echo "Creating __init__.py files for Python packages..."
find $BUILD_DIR/usr/lib/$APP_NAME -type d -exec touch {}/__init__.py \; 2>/dev/null || true

# Создаем ИСПРАВЛЕННЫЕ версии проблемных модулей с правильными именами классов
echo "Creating fixed versions of problematic modules..."

echo "Creating simple launcher script..."
cat > $BUILD_DIR/usr/lib/$APP_NAME/launcher.py << 'EOF'
#!/usr/bin/env python3
import os
import sys
import shutil
import traceback

def setup_environment():
    """Setup environment with proper database path"""
    # Use home directory for compatibility
    data_dir = os.path.expanduser("~/.permix")
    os.makedirs(data_dir, exist_ok=True)

    # Copy database if needed
    system_db = "/usr/lib/permix/data.db"
    user_db = os.path.join(data_dir, "data.db")

    if not os.path.exists(user_db):
        try:
            shutil.copy2(system_db, user_db)
            print(f"Database copied to: {user_db}")
        except Exception as e:
            print(f"Error copying database: {e}")
            user_db = system_db  # Fallback

    # Set environment variable
    os.environ["PERMIX_DATABASE_PATH"] = user_db
    print(f"Using database: {user_db}")
    return user_db

if __name__ == "__main__":
    # Setup environment
    db_path = setup_environment()

    # Add to Python path
    sys.path.insert(0, "/usr/lib/permix")

    try:
        # Import and explicitly run the application
        from main import App, init_database

        # Initialize database and start GUI
        init_database()
        app = App()
        app.mainloop()

    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
        input("Press Enter to exit...")
EOF

# Анализируем requirements.txt для определения зависимостей Debian
echo "Analyzing requirements.txt for dependencies..."
REQUIREMENTS_FILE="$WINDOWS_PROJECT_PATH/requirements.txt"
DEB_DEPENDS="python3, python3-tk, python3-periodictable"

if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "Found requirements.txt, analyzing dependencies..."

    while IFS= read -r line; do
        line=$(echo "$line" | sed 's/#.*//' | xargs)

        if [ -n "$line" ]; then
            case "$line" in
                pandas*)
                    DEB_DEPENDS="$DEB_DEPENDS, python3-pandas"
                    ;;
                numpy*)
                    DEB_DEPENDS="$DEB_DEPENDS, python3-numpy"
                    ;;
                SQLAlchemy*|sqlalchemy*)
                    DEB_DEPENDS="$DEB_DEPENDS, python3-sqlalchemy"
                    ;;
                openpyxl*)
                    DEB_DEPENDS="$DEB_DEPENDS, python3-openpyxl"
                    ;;
                matplotlib*)
                    DEB_DEPENDS="$DEB_DEPENDS, python3-matplotlib"
                    ;;
                scipy*)
                    DEB_DEPENDS="$DEB_DEPENDS, python3-scipy"
                    ;;
                Pillow*|pillow*)
                    DEB_DEPENDS="$DEB_DEPENDS, python3-pil"
                    ;;
                periodictable*)
                    DEB_DEPENDS="$DEB_DEPENDS, python3-periodictable"
                    ;;
                tkinter*)
                    ;;
                *)
                    echo "Note: Package '$line' might need manual mapping to Debian package"
                    ;;
            esac
        fi
    done < "$REQUIREMENTS_FILE"

    echo "Resolved dependencies: $DEB_DEPENDS"
else
    echo "No requirements.txt found, using basic dependencies"
fi

# Создаем copyright файл
echo "Creating copyright file..."
cat > $BUILD_DIR/usr/share/doc/$APP_NAME/copyright << 'EOF'
Format: https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
Upstream-Name: PerMix
Source: https://github.com/your-repo/permix

Files: *
Copyright: 2024 Schmidberskaya & Simonenko
License: MIT

License: MIT
 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:
 .
 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.
 .
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 SOFTWARE.
EOF

# Создаем changelog
echo "Creating changelog..."
cat > $BUILD_DIR/usr/share/doc/$APP_NAME/changelog.Debian << EOF
permix ($VERSION) unstable; urgency=medium

  * Fixed class name in database module (LocalizationDB)
  * Fixed database path issues with environment variables
  * Uses /tmp/permix_data/ for WSL compatibility

 -- Schmidberskaya & Simonenko <shap.20@uni-dubna.ru>  $(date -R)
EOF
gzip -9n $BUILD_DIR/usr/share/doc/$APP_NAME/changelog.Debian

# Создаем файл control
echo "Creating control file..."
cat > $BUILD_DIR/DEBIAN/control << EOF
Package: $APP_NAME
Version: $VERSION
Section: science
Priority: optional
Architecture: $ARCHITECTURE
Depends: $DEB_DEPENDS
Maintainer: $MAINTAINER
Description: Precursor Stoichiometry Calculator for Perovskite Synthesis
 PerMix is a graphical user interface application designed to address
 a critical bottleneck in materials science: the precise and reproducible
 calculation of precursor stoichiometry for multicomponent perovskite
 synthesis. It provides a standardized, high-precision tool to eliminate
 a major source of experimental variation, allowing for more reliable
 comparison of results between different laboratories and studies.
EOF

# Создаем запускающий скрипт
echo "Creating launcher script..."
cat > $BUILD_DIR/usr/bin/$APP_NAME << 'EOF'
#!/bin/bash
cd /usr/lib/permix
python3 launcher.py "$@"
EOF

# Создаем desktop файл
echo "Creating desktop file..."
cat > $BUILD_DIR/usr/share/applications/$APP_NAME.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=PerMix
Comment=Precursor Stoichiometry Calculator for Perovskite Synthesis
Exec=permix
Icon=permix
Terminal=false
Categories=Science;Education;
Keywords=perovskite;materials;science;chemistry;stoichiometry;
StartupNotify=true
EOF

# Устанавливаем правильные права
echo "Setting permissions..."
find $BUILD_DIR -type d -exec chmod 755 {} \;
find $BUILD_DIR -type f -exec chmod 644 {} \;
chmod 755 $BUILD_DIR/usr/bin/$APP_NAME
chmod 755 $BUILD_DIR/usr/lib/$APP_NAME/launcher.py

# Устанавливаем правильного владельца и собираем пакет
echo "Setting file ownership and building package..."
fakeroot bash -c "
    chown -R root:root $BUILD_DIR
    dpkg-deb --build $BUILD_DIR ${APP_NAME}_${VERSION}_${ARCHITECTURE}.deb
"

# Проверяем успешность сборки
if [ -f "${APP_NAME}_${VERSION}_${ARCHITECTURE}.deb" ]; then
    cp "${APP_NAME}_${VERSION}_${ARCHITECTURE}.deb" "$WINDOWS_PROJECT_PATH/"

    echo "=== DEB package created successfully: ${APP_NAME}_${VERSION}_${ARCHITECTURE}.deb ==="
    echo "Package copied to: $WINDOWS_PROJECT_PATH/"

    echo ""
    echo "📋 Resolved dependencies:"
    echo "   $DEB_DEPENDS"
    echo ""
    echo "✅ Installation instructions:"
    echo "1. Remove old version: sudo dpkg --purge permix"
    echo "2. Install: sudo apt install ./${APP_NAME}_${VERSION}_${ARCHITECTURE}.deb"
    echo "3. Run: permix"

else
    echo "=== ERROR: DEB package was not created! ==="
fi

rm -rf $BUILD_DIR