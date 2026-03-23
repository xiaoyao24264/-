#!/usr/bin/env python3
"""
Dota2 战队排名爬虫 - OpenDota API
支持: 全球战队排名、近期比赛、联赛数据
"""

import requests
import json
import time
from datetime import datetime

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json',
}

BASE_URL = 'https://api.opendota.com/api'

def get_team_rankings(limit=50):
    """获取战队排名（按胜场排序）"""
    try:
        resp = requests.get(f'{BASE_URL}/teams', headers=HEADERS, timeout=30)
        resp.raise_for_status()
        teams = resp.json()
        
        # 按胜场排序
        sorted_teams = sorted(teams, key=lambda x: x.get('wins', 0), reverse=True)[:limit]
        
        result = []
        for i, t in enumerate(sorted_teams):
            wins = t.get('wins', 0)
            losses = t.get('losses', 0)
            total = wins + losses
            winrate = f"{wins/total*100:.1f}%" if total > 0 else "0%"
            
            result.append({
                'rank': i + 1,
                'team_id': t.get('team_id'),
                'name': t.get('name', 'Unknown'),
                'tag': t.get('tag', ''),
                'wins': wins,
                'losses': losses,
                'win_rate': winrate,
                'rating': round(t.get('rating', 0), 1),
                'last_match': t.get('last_match_time'),
                'logo': t.get('logo_url', ''),
            })
        return result
    except Exception as e:
        print(f"[ERROR] get_team_rankings: {e}")
        return []

def get_recent_matches(limit=50):
    """获取近期职业比赛"""
    try:
        resp = requests.get(f'{BASE_URL}/proMatches', headers=HEADERS, timeout=30)
        resp.raise_for_status()
        matches = resp.json()[:limit]
        
        result = []
        for m in matches:
            radiant_win = m.get('radiant_win', False)
            radiant_score = m.get('radiant_score', 0)
            dire_score = m.get('dire_score', 0)
            
            # 判断哪方赢了
            if radiant_win:
                winner = m.get('radiant_name', 'Radiant')
                loser = m.get('dire_name', 'Dire')
            else:
                winner = m.get('dire_name', 'Dire')
                loser = m.get('radiant_name', 'Radiant')
            
            result.append({
                'match_id': m.get('match_id'),
                'league': m.get('league_name', 'Unknown'),
                'league_id': m.get('leagueid'),
                'start_time': m.get('start_time'),
                'winner': winner,
                'loser': loser,
                'score': f"{radiant_score} - {dire_score}",
                'duration': m.get('duration'),
                'series_type': m.get('series_type', 0),
            })
        return result
    except Exception as e:
        print(f"[ERROR] get_recent_matches: {e}")
        return []

def get_leagues():
    """获取主要联赛列表"""
    try:
        resp = requests.get(f'{BASE_URL}/leagues', headers=HEADERS, timeout=30)
        resp.raise_for_status()
        leagues = resp.json()
        
        # 只保留有 tier 的联赛
        major_leagues = [l for l in leagues if l.get('tier') in ['premium', 'professional']]
        
        result = []
        for l in major_leagues[:30]:
            result.append({
                'league_id': l.get('leagueid'),
                'name': l.get('name', 'Unknown'),
                'tier': l.get('tier', ''),
            })
        return result
    except Exception as e:
        print(f"[ERROR] get_leagues: {e}")
        return []

def crawl_all():
    """爬取所有数据"""
    print("=" * 60)
    print("Dota2 数据爬虫 - OpenDota API")
    print("=" * 60)
    print()
    
    print("[1/3] 正在获取战队排名...")
    teams = get_team_rankings(50)
    print(f"      ✓ 获取到 {len(teams)} 支战队")
    
    print("[2/3] 正在获取近期比赛...")
    matches = get_recent_matches(50)
    print(f"      ✓ 获取到 {len(matches)} 场比赛")
    
    print("[3/3] 正在获取联赛信息...")
    leagues = get_leagues()
    print(f"      ✓ 获取到 {len(leagues)} 个联赛")
    
    return {
        'fetched_at': datetime.now().isoformat(),
        'source': 'OpenDota API',
        'teams': teams,
        'recent_matches': matches,
        'leagues': leagues,
    }

def save_json(data, filepath):
    """保存 JSON 文件"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\n已保存到 {filepath}")

if __name__ == '__main__':
    data = crawl_all()
    
    print()
    print("=" * 60)
    print(f"战队 TOP 10:")
    print("=" * 60)
    for t in data['teams'][:10]:
        print(f"  {t['rank']:2}. {t['name']:<20} {t['wins']}W/{t['losses']}L ({t['win_rate']})")
    
    print()
    print("=" * 60)
    print(f"近期比赛 TOP 5:")
    print("=" * 60)
    for m in data['recent_matches'][:5]:
        print(f"  {m['league']}: {m['winner']} 胜 {m['loser']} ({m['score']})")
    
    save_json(data, '/root/esports-data/dota2_data.json')
