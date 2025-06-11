"""
Save/load system with compression
"""

import pickle
import gzip
import json
import os
from typing import Any, Dict
from datetime import datetime

class SaveSystem:
    """Handle saving and loading game state with compression"""
    
    def __init__(self, save_directory: str = "saves"):
        self.save_directory = save_directory
        self._ensure_save_directory()
        
    def _ensure_save_directory(self):
        """Create save directory if it doesn't exist"""
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)
            
    def save(self, game_state: Dict[str, Any], filename: str, compress: bool = True):
        """Save game state to file"""
        filepath = os.path.join(self.save_directory, filename)
        
        # Add metadata
        save_data = {
            'metadata': {
                'version': '1.0',
                'timestamp': datetime.now().isoformat(),
                'compressed': compress
            },
            'game_state': game_state
        }
        
        if compress:
            # Save with gzip compression
            with gzip.open(filepath, 'wb') as f:
                pickle.dump(save_data, f, protocol=pickle.HIGHEST_PROTOCOL)
        else:
            # Save without compression
            with open(filepath, 'wb') as f:
                pickle.dump(save_data, f, protocol=pickle.HIGHEST_PROTOCOL)
                
        print(f"Game saved to {filepath}")
        
    def load(self, filename: str) -> Dict[str, Any]:
        """Load game state from file"""
        filepath = os.path.join(self.save_directory, filename)
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Save file not found: {filepath}")
            
        try:
            # Try loading as compressed first
            with gzip.open(filepath, 'rb') as f:
                save_data = pickle.load(f)
        except (gzip.BadGzipFile, OSError):
            # If that fails, try uncompressed
            with open(filepath, 'rb') as f:
                save_data = pickle.load(f)
                
        # Validate save data
        if 'game_state' not in save_data:
            raise ValueError("Invalid save file format")
            
        print(f"Game loaded from {filepath}")
        return save_data['game_state']
        
    def list_saves(self) -> list:
        """List all available save files"""
        saves = []
        
        for filename in os.listdir(self.save_directory):
            filepath = os.path.join(self.save_directory, filename)
            if os.path.isfile(filepath):
                try:
                    # Get file info
                    stat = os.stat(filepath)
                    size_mb = stat.st_size / (1024 * 1024)
                    modified = datetime.fromtimestamp(stat.st_mtime)
                    
                    saves.append({
                        'filename': filename,
                        'size_mb': round(size_mb, 2),
                        'modified': modified.isoformat(),
                        'path': filepath
                    })
                except Exception as e:
                    print(f"Error reading save file {filename}: {e}")
                    
        # Sort by modification time (newest first)
        saves.sort(key=lambda x: x['modified'], reverse=True)
        return saves
        
    def delete_save(self, filename: str) -> bool:
        """Delete a save file"""
        filepath = os.path.join(self.save_directory, filename)
        
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                print(f"Deleted save file: {filename}")
                return True
            except Exception as e:
                print(f"Error deleting save file {filename}: {e}")
                return False
        else:
            print(f"Save file not found: {filename}")
            return False
            
    def get_save_info(self, filename: str) -> Dict[str, Any]:
        """Get information about a save file"""
        filepath = os.path.join(self.save_directory, filename)
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Save file not found: {filepath}")
            
        # Get file stats
        stat = os.stat(filepath)
        info = {
            'filename': filename,
            'size_bytes': stat.st_size,
            'size_mb': round(stat.st_size / (1024 * 1024), 2),
            'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
            'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
        }
        
        # Try to read metadata
        try:
            if filename.endswith('.gz') or self._is_gzipped(filepath):
                with gzip.open(filepath, 'rb') as f:
                    save_data = pickle.load(f)
            else:
                with open(filepath, 'rb') as f:
                    save_data = pickle.load(f)
                    
            if 'metadata' in save_data:
                info['metadata'] = save_data['metadata']
                
        except Exception as e:
            info['error'] = f"Could not read save metadata: {e}"
            
        return info
        
    def _is_gzipped(self, filepath: str) -> bool:
        """Check if file is gzip compressed"""
        try:
            with gzip.open(filepath, 'rb') as f:
                f.read(1)
            return True
        except (gzip.BadGzipFile, OSError):
            return False
            
    def export_save_info(self, filename: str, output_file: str):
        """Export save file information to JSON"""
        try:
            info = self.get_save_info(filename)
            
            with open(output_file, 'w') as f:
                json.dump(info, f, indent=2, default=str)
                
            print(f"Save info exported to {output_file}")
            
        except Exception as e:
            print(f"Error exporting save info: {e}")
            
    def backup_save(self, filename: str) -> str:
        """Create a backup copy of a save file"""
        filepath = os.path.join(self.save_directory, filename)
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Save file not found: {filepath}")
            
        # Create backup filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"{filename}.backup_{timestamp}"
        backup_filepath = os.path.join(self.save_directory, backup_filename)
        
        # Copy file
        import shutil
        shutil.copy2(filepath, backup_filepath)
        
        print(f"Backup created: {backup_filename}")
        return backup_filename
