import os
import uuid
import json
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# 数据库配置
DATABASE = 'accounts.db'

def get_db():
    """获取数据库连接"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """初始化数据库表"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS account_links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT UNIQUE NOT NULL,
            accounts TEXT NOT NULL,
            expire_at INTEGER NOT NULL,
            created_at INTEGER NOT NULL,
            is_active BOOLEAN DEFAULT 1,
            one_time BOOLEAN DEFAULT 0,
            allow_destroy BOOLEAN DEFAULT 0,
            view_password TEXT DEFAULT NULL
        )
    ''')
    conn.commit()
    conn.close()

def cleanup_expired():
    """清理过期的链接"""
    conn = get_db()
    cursor = conn.cursor()
    current_time = int(datetime.now().timestamp())
    cursor.execute(
        'UPDATE account_links SET is_active = 0 WHERE expire_at < ?',
        (current_time,)
    )
    conn.commit()
    conn.close()

# API 路由

@app.route('/api/create', methods=['POST'])
def create_link():
    """创建账号分发链接"""
    try:
        data = request.get_json()

        # 参数校验
        if not data:
            return jsonify({'error': '请求数据为空'}), 400

        accounts_text = data.get('accounts', '').strip()
        expire_hours = data.get('expire_hours', 24)
        one_time = data.get('one_time', False)
        allow_destroy = data.get('allow_destroy', False)
        view_password = data.get('view_password', '').strip()

        if not accounts_text:
            return jsonify({'error': '内容不能为空'}), 400

        try:
            expire_hours = float(expire_hours)
            if expire_hours <= 0 or expire_hours > 24:  # 最多24小时
                return jsonify({'error': '有效期必须在0.5-24小时之间'}), 400
        except ValueError:
            return jsonify({'error': '有效期必须是数字'}), 400

        # 过滤HTML标签
        import re
        # 移除HTML标签
        accounts_text = re.sub(r'<[^>]+>', '', accounts_text)
        # 移除HTML实体
        html_entities = {
            '&lt;': '<',
            '&gt;': '>',
            '&amp;': '&',
            '&quot;': '"',
            '&apos;': "'",
            '&nbsp;': ' '
        }
        for entity, char in html_entities.items():
            accounts_text = accounts_text.replace(entity, char)

        # 生成UUID和计算过期时间
        link_uuid = str(uuid.uuid4())
        current_time = int(datetime.now().timestamp())
        expire_time = current_time + (expire_hours * 3600)

        # 存储到数据库（直接存储原始文本）
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO account_links (uuid, accounts, expire_at, created_at, is_active, one_time, allow_destroy, view_password)
               VALUES (?, ?, ?, ?, 1, ?, ?, ?)''',
            (link_uuid, accounts_text, expire_time, current_time, one_time, allow_destroy, view_password if view_password else None)
        )
        conn.commit()
        conn.close()

        return jsonify({
            'success': True,
            'uuid': link_uuid,
            'link': f'/link/{link_uuid}'
        }), 200

    except Exception as e:
        print(f"Error creating link: {e}")
        return jsonify({'error': '创建链接失败'}), 500


@app.route('/api/link/<uuid>', methods=['GET'])
def get_link(uuid):
    """获取链接内容"""
    try:
        cleanup_expired()

        # 获取密码参数
        password = request.args.get('password', '').strip()

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT accounts, expire_at, is_active, one_time, allow_destroy, view_password FROM account_links WHERE uuid = ?',
            (uuid,)
        )
        row = cursor.fetchone()
        conn.close()

        if not row:
            return jsonify({'error': '链接不存在'}), 404

        if not row['is_active']:
            return jsonify({'status': 'expired', 'message': '链接已失效'}), 200

        # 检查是否过期
        current_time = int(datetime.now().timestamp())
        if current_time > row['expire_at']:
            return jsonify({'status': 'expired', 'message': '链接已过期'}), 200

        # 验证密码
        if row['view_password']:
            if not password:
                return jsonify({'status': 'password_required', 'message': '需要输入密码'}), 200
            if password != row['view_password']:
                return jsonify({'status': 'password_error', 'message': '密码错误'}), 200

        # 返回账号数据
        accounts_text = row['accounts']
        remaining_seconds = row['expire_at'] - current_time
        remaining_hours = max(0, remaining_seconds / 3600)

        # 如果是一次性链接，立即失效
        if row['one_time']:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE account_links SET is_active = 0 WHERE uuid = ?',
                (uuid,)
            )
            conn.commit()
            conn.close()

        return jsonify({
            'status': 'active',
            'content': accounts_text,
            'remaining_hours': round(remaining_hours, 2),
            'one_time': row['one_time'],
            'allow_destroy': row['allow_destroy'],
            'has_password': bool(row['view_password'])
        }), 200

    except Exception as e:
        print(f"Error getting link: {e}")
        return jsonify({'error': '获取链接失败'}), 500


@app.route('/api/status/<uuid>', methods=['GET'])
def check_status(uuid):
    """检查链接状态"""
    try:
        cleanup_expired()

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT expire_at, is_active FROM account_links WHERE uuid = ?',
            (uuid,)
        )
        row = cursor.fetchone()
        conn.close()

        if not row:
            return jsonify({'exists': False}), 404

        if not row['is_active']:
            return jsonify({
                'exists': True,
                'active': False,
                'status': 'expired'
            }), 200

        current_time = int(datetime.now().timestamp())
        if current_time > row['expire_at']:
            return jsonify({
                'exists': True,
                'active': False,
                'status': 'expired'
            }), 200

        remaining_seconds = row['expire_at'] - current_time
        remaining_hours = max(0, remaining_seconds / 3600)

        return jsonify({
            'exists': True,
            'active': True,
            'status': 'active',
            'remaining_hours': round(remaining_hours, 2)
        }), 200

    except Exception as e:
        print(f"Error checking status: {e}")
        return jsonify({'error': '检查状态失败'}), 500


@app.route('/api/link/<uuid>', methods=['DELETE'])
def deactivate_link(uuid):
    """使链接失效"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE account_links SET is_active = 0 WHERE uuid = ?',
            (uuid,)
        )
        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': '链接已失效'}), 200

    except Exception as e:
        print(f"Error deactivating link: {e}")
        return jsonify({'error': '失效链接失败'}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({'status': 'ok'}), 200


if __name__ == '__main__':
    init_db()
    print("Prime Account Dist Backend API 启动成功")
    print("数据库已初始化")
    app.run(debug=True, host='0.0.0.0', port=5000)