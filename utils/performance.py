"""
Performance monitoring utilities
"""

import time
import psutil
import os
from typing import Dict, List, Any
from collections import deque

class PerformanceMonitor:
    """Monitor and track performance metrics"""
    
    def __init__(self, history_size: int = 60):
        self.history_size = history_size
        
        # Frame timing
        self.frame_times = deque(maxlen=history_size)
        self.frame_start_time = 0
        
        # System metrics
        self.cpu_usage_history = deque(maxlen=history_size)
        self.memory_usage_history = deque(maxlen=history_size)
        
        # Game-specific metrics
        self.entity_count_history = deque(maxlen=history_size)
        self.pathfinding_calls = 0
        self.pathfinding_time = 0
        
        # Process handle
        self.process = psutil.Process(os.getpid())
        
    def start_frame(self):
        """Mark the start of a frame"""
        self.frame_start_time = time.time()
        
    def end_frame(self):
        """Mark the end of a frame and record metrics"""
        if self.frame_start_time > 0:
            frame_time = time.time() - self.frame_start_time
            self.frame_times.append(frame_time)
            
        # Record system metrics
        self.cpu_usage_history.append(self.process.cpu_percent())
        memory_mb = self.process.memory_info().rss / 1024 / 1024
        self.memory_usage_history.append(memory_mb)
        
    def get_average_fps(self) -> float:
        """Get average FPS over recent frames"""
        if not self.frame_times:
            return 0.0
            
        avg_frame_time = sum(self.frame_times) / len(self.frame_times)
        return 1.0 / avg_frame_time if avg_frame_time > 0 else 0.0
        
    def get_frame_time_stats(self) -> Dict[str, float]:
        """Get frame time statistics"""
        if not self.frame_times:
            return {'min': 0, 'max': 0, 'avg': 0, 'current': 0}
            
        frame_times_list = list(self.frame_times)
        return {
            'min': min(frame_times_list) * 1000,  # Convert to ms
            'max': max(frame_times_list) * 1000,
            'avg': (sum(frame_times_list) / len(frame_times_list)) * 1000,
            'current': frame_times_list[-1] * 1000 if frame_times_list else 0
        }
        
    def get_memory_stats(self) -> Dict[str, float]:
        """Get memory usage statistics"""
        if not self.memory_usage_history:
            return {'current': 0, 'peak': 0, 'avg': 0}
            
        memory_list = list(self.memory_usage_history)
        return {
            'current': memory_list[-1] if memory_list else 0,
            'peak': max(memory_list),
            'avg': sum(memory_list) / len(memory_list)
        }
        
    def get_cpu_stats(self) -> Dict[str, float]:
        """Get CPU usage statistics"""
        if not self.cpu_usage_history:
            return {'current': 0, 'peak': 0, 'avg': 0}
            
        cpu_list = list(self.cpu_usage_history)
        return {
            'current': cpu_list[-1] if cpu_list else 0,
            'peak': max(cpu_list),
            'avg': sum(cpu_list) / len(cpu_list)
        }
        
    def record_pathfinding_call(self, execution_time: float):
        """Record a pathfinding call"""
        self.pathfinding_calls += 1
        self.pathfinding_time += execution_time
        
    def get_pathfinding_stats(self) -> Dict[str, Any]:
        """Get pathfinding performance statistics"""
        avg_time = (self.pathfinding_time / self.pathfinding_calls 
                   if self.pathfinding_calls > 0 else 0)
        
        return {
            'total_calls': self.pathfinding_calls,
            'total_time': self.pathfinding_time,
            'avg_time_ms': avg_time * 1000
        }
        
    def reset_pathfinding_stats(self):
        """Reset pathfinding statistics"""
        self.pathfinding_calls = 0
        self.pathfinding_time = 0
        
    def get_performance_report(self) -> Dict[str, Any]:
        """Get comprehensive performance report"""
        return {
            'fps': {
                'current': 1.0 / self.frame_times[-1] if self.frame_times else 0,
                'average': self.get_average_fps()
            },
            'frame_time': self.get_frame_time_stats(),
            'memory': self.get_memory_stats(),
            'cpu': self.get_cpu_stats(),
            'pathfinding': self.get_pathfinding_stats()
        }
        
    def is_performance_acceptable(self, target_fps: int = 60, 
                                max_memory_mb: int = 2048) -> bool:
        """Check if performance meets acceptable thresholds"""
        current_fps = self.get_average_fps()
        current_memory = self.get_memory_stats()['current']
        
        return (current_fps >= target_fps * 0.8 and  # Allow 20% below target
                current_memory <= max_memory_mb)
                
    def get_performance_warnings(self, target_fps: int = 60, 
                               max_memory_mb: int = 2048) -> List[str]:
        """Get list of performance warnings"""
        warnings = []
        
        current_fps = self.get_average_fps()
        if current_fps < target_fps * 0.5:
            warnings.append(f"Low FPS: {current_fps:.1f} (target: {target_fps})")
            
        memory_stats = self.get_memory_stats()
        if memory_stats['current'] > max_memory_mb * 0.9:
            warnings.append(f"High memory usage: {memory_stats['current']:.1f}MB")
            
        cpu_stats = self.get_cpu_stats()
        if cpu_stats['current'] > 80:
            warnings.append(f"High CPU usage: {cpu_stats['current']:.1f}%")
            
        frame_stats = self.get_frame_time_stats()
        if frame_stats['max'] > 50:  # 50ms = 20 FPS
            warnings.append(f"Frame time spikes: {frame_stats['max']:.1f}ms")
            
        return warnings
