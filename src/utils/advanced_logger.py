#!/usr/bin/env python3
"""
Sistema de logging avanzado para PyGame Shooter
Autor: Kava
Fecha: 2024-12-19
Descripción: Sistema completo de logging modular y profesional para todos los componentes del juego, usando logging nativo de Python.
"""

import logging
import logging.handlers
import os
import sys
from datetime import datetime
from typing import Optional, Dict, Any
from pathlib import Path


class AdvancedLogger:
    """
    Sistema de logging avanzado usando logging nativo de Python.
    Proporciona múltiples archivos de log, niveles, formato personalizado y logging en consola.
    """
    
    def __init__(self, name: str = "PyGame", log_dir: str = "logs"):
        """
        Inicializa el sistema de logging avanzado.
        
        Args:
            name: Nombre del logger principal
            log_dir: Directorio donde guardar los logs
        """
        self.name = name
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Configurar el logger principal
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Evitar duplicación de handlers
        if not self.logger.handlers:
            self._setup_handlers()
        
        # Loggers específicos por componente
        self.component_loggers: Dict[str, logging.Logger] = {}
        
        self.logger.info(f"Sistema de logging avanzado inicializado - Directorio: {self.log_dir}")
    
    def _setup_handlers(self) -> None:
        """Configura los handlers para el logger principal."""
        
        # Handler para consola (solo INFO y superior)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # Handler para archivo general (todos los niveles)
        general_handler = logging.handlers.RotatingFileHandler(
            self.log_dir / "game.log",
            maxBytes=1024*1024,  # 1MB
            backupCount=5,
            encoding='utf-8'
        )
        general_handler.setLevel(logging.DEBUG)
        general_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        general_handler.setFormatter(general_formatter)
        self.logger.addHandler(general_handler)
        
        # Handler para errores (solo ERROR y CRITICAL)
        error_handler = logging.handlers.RotatingFileHandler(
            self.log_dir / "errors.log",
            maxBytes=512*1024,  # 512KB
            backupCount=3,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s\n'
            'Exception: %(exc_info)s\n',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        error_handler.setFormatter(error_formatter)
        self.logger.addHandler(error_handler)
    
    def get_component_logger(self, component_name: str) -> logging.Logger:
        """
        Obtiene o crea un logger específico para un componente.
        
        Args:
            component_name: Nombre del componente (ej: 'menu', 'player', 'enemy')
            
        Returns:
            Logger específico del componente
        """
        if component_name not in self.component_loggers:
            # Crear logger específico
            component_logger = logging.getLogger(f"{self.name}.{component_name}")
            component_logger.setLevel(logging.DEBUG)
            
            # Handler específico para el componente
            component_handler = logging.handlers.RotatingFileHandler(
                self.log_dir / f"{component_name}.log",
                maxBytes=512*1024,  # 512KB
                backupCount=3,
                encoding='utf-8'
            )
            component_handler.setLevel(logging.DEBUG)
            component_formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            component_handler.setFormatter(component_formatter)
            component_logger.addHandler(component_handler)
            
            self.component_loggers[component_name] = component_logger
            self.logger.info(f"Logger creado para componente: {component_name}")
        
        return self.component_loggers[component_name]
    
    def log_event(self, message: str, component: Optional[str] = None) -> None:
        """
        Registra un evento informativo.
        
        Args:
            message: Mensaje del evento
            component: Componente específico (opcional)
        """
        if component:
            self.get_component_logger(component).info(message)
        else:
            self.logger.info(message)
    
    def log_debug(self, message: str, component: Optional[str] = None) -> None:
        """
        Registra un mensaje de debug.
        
        Args:
            message: Mensaje de debug
            component: Componente específico (opcional)
        """
        if component:
            self.get_component_logger(component).debug(message)
        else:
            self.logger.debug(message)
    
    def log_warning(self, message: str, component: Optional[str] = None) -> None:
        """
        Registra una advertencia.
        
        Args:
            message: Mensaje de advertencia
            component: Componente específico (opcional)
        """
        if component:
            self.get_component_logger(component).warning(message)
        else:
            self.logger.warning(message)
    
    def log_error(self, message: str, component: Optional[str] = None, exc_info: bool = True) -> None:
        """
        Registra un error.
        
        Args:
            message: Mensaje de error
            component: Componente específico (opcional)
            exc_info: Si incluir información de excepción
        """
        if component:
            self.get_component_logger(component).error(message, exc_info=exc_info)
        else:
            self.logger.error(message, exc_info=exc_info)
    
    def log_critical(self, message: str, component: Optional[str] = None, exc_info: bool = True) -> None:
        """
        Registra un error crítico.
        
        Args:
            message: Mensaje de error crítico
            component: Componente específico (opcional)
            exc_info: Si incluir información de excepción
        """
        if component:
            self.get_component_logger(component).critical(message, exc_info=exc_info)
        else:
            self.logger.critical(message, exc_info=exc_info)
    
    def log_performance(self, operation: str, duration: float, component: Optional[str] = None) -> None:
        """
        Registra métricas de rendimiento.
        
        Args:
            operation: Nombre de la operación
            duration: Duración en segundos
            component: Componente específico (opcional)
        """
        message = f"PERFORMANCE - {operation}: {duration:.4f}s"
        if component:
            self.get_component_logger(component).info(message)
        else:
            self.logger.info(message)
    
    def log_game_event(self, event_type: str, event_data: Dict[str, Any], component: Optional[str] = None) -> None:
        """
        Registra eventos específicos del juego.
        
        Args:
            event_type: Tipo de evento (ej: 'player_move', 'enemy_spawn', 'score_update')
            event_data: Datos del evento
            component: Componente específico (opcional)
        """
        message = f"GAME_EVENT - {event_type}: {event_data}"
        if component:
            self.get_component_logger(component).info(message)
        else:
            self.logger.info(message)
    
    def log_user_action(self, action: str, details: Optional[Dict[str, Any]] = None, component: Optional[str] = None) -> None:
        """
        Registra acciones del usuario.
        
        Args:
            action: Acción realizada
            details: Detalles adicionales
            component: Componente específico (opcional)
        """
        message = f"USER_ACTION - {action}"
        if details:
            message += f": {details}"
        
        if component:
            self.get_component_logger(component).info(message)
        else:
            self.logger.info(message)
    
    def log_system_info(self) -> None:
        """Registra información del sistema."""
        import platform
        import pygame
        
        system_info = {
            'platform': platform.platform(),
            'python_version': platform.python_version(),
            'pygame_version': pygame.version.ver,
            'pygame_ce': hasattr(pygame, 'version'),
            'cpu_count': os.cpu_count(),
            'memory_available': self._get_memory_info()
        }
        
        self.logger.info(f"SYSTEM_INFO: {system_info}")
    
    def _get_memory_info(self) -> Dict[str, Any]:
        """Obtiene información de memoria del sistema."""
        try:
            import psutil
            memory = psutil.virtual_memory()
            return {
                'total': f"{memory.total / (1024**3):.1f}GB",
                'available': f"{memory.available / (1024**3):.1f}GB",
                'percent': f"{memory.percent}%"
            }
        except ImportError:
            return {'error': 'psutil no disponible'}
    
    def set_level(self, level: str, component: Optional[str] = None) -> None:
        """
        Establece el nivel de logging.
        
        Args:
            level: Nivel ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
            component: Componente específico (opcional)
        """
        level_map = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        
        log_level = level_map.get(level.upper(), logging.INFO)
        
        if component:
            self.get_component_logger(component).setLevel(log_level)
        else:
            self.logger.setLevel(log_level)
        
        self.logger.info(f"Nivel de logging establecido: {level} para {component or 'general'}")
    
    def clear_logs(self, component: Optional[str] = None) -> None:
        """
        Limpia los archivos de log.
        
        Args:
            component: Componente específico (opcional)
        """
        if component:
            log_file = self.log_dir / f"{component}.log"
            if log_file.exists():
                log_file.unlink()
                self.logger.info(f"Log limpiado para componente: {component}")
        else:
            # Limpiar todos los logs
            for log_file in self.log_dir.glob("*.log"):
                log_file.unlink()
            self.logger.info("Todos los logs han sido limpiados")
    
    def get_log_stats(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de los archivos de log.
        
        Returns:
            Diccionario con estadísticas de logs
        """
        stats = {
            'total_files': 0,
            'total_size': 0,
            'files': {}
        }
        
        for log_file in self.log_dir.glob("*.log"):
            stats['total_files'] += 1
            size = log_file.stat().st_size
            stats['total_size'] += size
            stats['files'][log_file.name] = {
                'size': size,
                'size_mb': f"{size / (1024**2):.2f}MB",
                'modified': datetime.fromtimestamp(log_file.stat().st_mtime).isoformat()
            }
        
        return stats
    
    def __str__(self) -> str:
        """Representación en string del logger."""
        return f"AdvancedLogger(name='{self.name}', log_dir='{self.log_dir}')"
    
    def __repr__(self) -> str:
        """Representación detallada del logger."""
        stats = self.get_log_stats()
        return f"AdvancedLogger(name='{self.name}', log_dir='{self.log_dir}', files={stats['total_files']})"


# Instancia global del logger
_global_logger: Optional[AdvancedLogger] = None

def get_logger(name: str = "PyGame") -> AdvancedLogger:
    """
    Obtiene la instancia global del logger.
    
    Args:
        name: Nombre del logger
        
    Returns:
        Instancia del AdvancedLogger
    """
    global _global_logger
    if _global_logger is None:
        _global_logger = AdvancedLogger(name)
    return _global_logger

def setup_logging(name: str = "PyGame", log_dir: str = "logs") -> AdvancedLogger:
    """
    Configura el sistema de logging global.
    
    Args:
        name: Nombre del logger
        log_dir: Directorio de logs
        
    Returns:
        Instancia del AdvancedLogger configurado
    """
    global _global_logger
    _global_logger = AdvancedLogger(name, log_dir)
    return _global_logger 