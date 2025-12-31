import os
import json
import random
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.animation import Animation
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import FloatLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.toast import toast

class SoundEffects:
    """Windows için ses efektleri"""
    
    @staticmethod
    def play_click():
        """Tıklama sesi"""
        try:
            import winsound
            winsound.Beep(800, 100)
        except:
            pass
    
    @staticmethod
    def play_success():
        """Başarı sesi"""
        try:
            import winsound
            winsound.Beep(1000, 200)
        except:
            pass
    
    @staticmethod
    def play_error():
        """Hata sesi"""
        try:
            import winsound
            winsound.Beep(400, 300)
        except:
            pass
    
    @staticmethod
    def play_level_up():
        """Seviye atlama sesi"""
        try:
            import winsound
            winsound.Beep(1200, 150)
            winsound.Beep(1500, 150)
        except:
            pass

class HomeScreen(Screen):
    pass

class GameScreen(Screen):
    pass

class GameOverScreen(Screen):
    pass

class WordCardApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.words = []
        self.score = 0
        self.level = 1
        self.difficulty_multiplier = 1.0
        self.current_question = None
        self.correct_option_index = 0
        self.high_score = 0
        self.current_index = 0
        self.used_words = []
    
    def build(self):
        """Uygulamayı oluştur"""
        print("Building application...")
        
        # KV kodunu yükle
        self.load_kv_code()
        
        # ScreenManager oluştur
        sm = ScreenManager()
        
        # Ekranları ekle
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(GameOverScreen(name='gameover'))
        
        print("Screens added to manager")
        return sm
    
    def load_kv_code(self):
        """KV kodunu yükle"""
        print("Loading KV code...")
        
        KV_CODE = """
<HomeScreen>:
    name: 'home'
    
    FloatLayout:
        # Gradient arka plan
        canvas.before:
            Color:
                rgba: (0.2, 0.6, 1.0, 1)
            Rectangle:
                pos: self.pos
                size: self.size
            Color:
                rgba: (1, 1, 1, 0.1)
            Rectangle:
                pos: self.pos
                size: self.size
        
        MDTopAppBar:
            title: "Kelime Challenge"
            elevation: 10
            pos_hint: {"top": 1}
            md_bg_color: app.theme_cls.primary_color
        
        MDBoxLayout:
            orientation: 'vertical'
            padding: 20
            spacing: 25
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            size_hint: 0.9, 0.8
            
            # İstatistik kartı
            MDCard:
                orientation: 'vertical'
                size_hint: 1, None
                height: 80
                padding: 15
                elevation: 8
                md_bg_color: (1, 1, 1, 0.9)
                
                MDLabel:
                    id: word_count_label
                    text: 'Toplam kelime yükleniyor...'
                    halign: 'center'
                    font_style: 'H6'
                    theme_text_color: 'Primary'
            
            # High score kartı
            MDCard:
                orientation: 'vertical'
                size_hint: 1, None
                height: 80
                padding: 15
                elevation: 8
                md_bg_color: (1, 1, 1, 0.9)
                
                MDLabel:
                    id: high_score_label
                    text: 'En Yüksek Skor: 0'
                    halign: 'center'
                    font_style: 'H6'
                    theme_text_color: 'Secondary'
            
            # Uyarı kartı
            MDCard:
                orientation: 'vertical'
                size_hint: 1, None
                height: 60
                padding: 10
                elevation: 6
                md_bg_color: (1, 0.9, 0.9, 0.9)
                
                MDLabel:
                    text: "Yanlış cevapta oyun biter!"
                    halign: 'center'
                    font_style: 'Body1'
                    theme_text_color: 'Error'
            
            MDRaisedButton:
                text: 'Challenge Başlat'
                size_hint: 0.8, None
                height: 48
                pos_hint: {"center_x": 0.5}
                on_release: 
                    app.animate_button(self)
                    root.manager.current = 'game'
                    app.start_challenge()
            
            MDRaisedButton:
                text: 'Tema Değiştir'
                size_hint: 0.8, None
                height: 48
                pos_hint: {"center_x": 0.5}
                md_bg_color: app.theme_cls.accent_color
                on_release: 
                    app.animate_button(self)
                    app.change_theme()

<GameScreen>:
    name: 'game'
    
    FloatLayout:
        MDTopAppBar:
            id: game_title
            title: "Puan: 0 | Seviye: 1"
            left_action_items: [["arrow-left", lambda x: setattr(root.manager, 'current', 'home')]]
            elevation: 10
            pos_hint: {"top": 1}
            md_bg_color: app.theme_cls.primary_color
        
        MDBoxLayout:
            orientation: 'vertical'
            padding: 20
            spacing: 20
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            size_hint: 0.9, 0.8
            
            MDCard:
                id: question_card
                orientation: 'vertical'
                size_hint: 1, None
                height: 200
                padding: 20
                spacing: 15
                elevation: 12
                md_bg_color: (1, 1, 1, 0.95)
                
                MDLabel:
                    id: question_label
                    text: 'İngilizce kelime'
                    halign: 'center'
                    font_style: 'H4'
                    theme_text_color: 'Primary'
                    size_hint: 1, None
                    height: 60
                
                MDLabel:
                    text: 'Türkçesi nedir?'
                    halign: 'center'
                    font_style: 'H6'
                    theme_text_color: 'Secondary'
                    size_hint: 1, None
                    height: 40
            
            MDBoxLayout:
                orientation: 'vertical'
                spacing: 10
                
                MDRaisedButton:
                    id: option1_btn
                    text: 'Seçenek 1'
                    size_hint: 1, None
                    height: 50
                    elevation: 8
                    on_release: app.check_answer(0)
                
                MDRaisedButton:
                    id: option2_btn
                    text: 'Seçenek 2'
                    size_hint: 1, None
                    height: 50
                    elevation: 8
                    on_release: app.check_answer(1)
                
                MDRaisedButton:
                    id: option3_btn
                    text: 'Seçenek 3'
                    size_hint: 1, None
                    height: 50
                    elevation: 8
                    on_release: app.check_answer(2)
                
                MDRaisedButton:
                    id: option4_btn
                    text: 'Seçenek 4'
                    size_hint: 1, None
                    height: 50
                    elevation: 8
                    on_release: app.check_answer(3)

<GameOverScreen>:
    name: 'gameover'
    
    FloatLayout:
        # Gradient arka plan
        canvas.before:
            Color:
                rgba: (0.8, 0.2, 0.2, 1)
            Rectangle:
                pos: self.pos
                size: self.size
            Color:
                rgba: (1, 1, 1, 0.1)
            Rectangle:
                pos: self.pos
                size: self.size
        
        MDTopAppBar:
            title: ""
            elevation: 0
            pos_hint: {"top": 1}
            md_bg_color: (0.8, 0.2, 0.2, 1)
        
        MDBoxLayout:
            orientation: 'vertical'
            padding: 20
            spacing: 25
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            size_hint: 0.9, 0.8
            
            # Sonuç kartı
            MDCard:
                orientation: 'vertical'
                size_hint: 1, None
                height: 220
                padding: 20
                spacing: 20
                elevation: 12
                md_bg_color: (1, 1, 1, 0.95)
                
                MDLabel:
                    text: "Yanlış Cevap!"
                    halign: 'center'
                    font_style: 'H4'
                    theme_text_color: 'Error'
                    size_hint: 1, None
                    height: 50
                
                MDLabel:
                    id: final_score_label
                    text: 'Puan: 0'
                    halign: 'center'
                    font_style: 'H5'
                    theme_text_color: 'Secondary'
                    size_hint: 1, None
                    height: 40
                
                MDLabel:
                    id: level_label
                    text: 'Seviye: 1'
                    halign: 'center'
                    font_style: 'Body1'
                    theme_text_color: 'Secondary'
                    size_hint: 1, None
                    height: 40
                
                MDLabel:
                    id: new_high_score_label
                    text: ''
                    halign: 'center'
                    font_style: 'H6'
                    theme_text_color: 'Primary'
                    size_hint: 1, None
                    height: 40
            
            MDRaisedButton:
                text: 'Tekrar Dene'
                size_hint: 0.8, None
                height: 48
                pos_hint: {"center_x": 0.5}
                elevation: 8
                on_release: 
                    app.animate_button(self)
                    root.manager.current = 'game'
                    app.start_challenge()
            
            MDRaisedButton:
                text: 'Ana Menü'
                size_hint: 0.8, None
                height: 48
                pos_hint: {"center_x": 0.5}
                elevation: 8
                on_release: 
                    app.animate_button(self)
                    root.manager.current = 'home'
"""
        
        Builder.load_string(KV_CODE)
        print("KV code loaded")
    
    def on_start(self):
        """Uygulama başladığında"""
        print("Application started")
        
        # Verileri yükle
        self.load_words()
        self.load_high_score()
        self.update_home_screen()
    
    def update_home_screen(self):
        """Ana ekranı güncelle"""
        try:
            print("Ana ekran güncelleniyor...")
            home_screen = self.root.get_screen('home')
            print(f"IDS: {home_screen.ids}")
            
            if hasattr(home_screen.ids, 'word_count_label'):
                home_screen.ids.word_count_label.text = f"Toplam {len(self.words)} kelime hazır!"
                print("word_count_label güncellendi")
            
            if hasattr(home_screen.ids, 'high_score_label'):
                home_screen.ids.high_score_label.text = f"En Yüksek Skor: {self.high_score}"
                print("high_score_label güncellendi")
            else:
                print("high_score_label bulunamadı!")
                
        except Exception as e:
            print(f"Ana ekran güncellenirken hata: {e}")
            import traceback
            traceback.print_exc()
    
    def load_words(self):
        """Kelimeleri JSON dosyasından yükle"""
        try:
            if os.path.exists('data/words.json'):
                with open('data/words.json', 'r', encoding='utf-8') as f:
                    self.words = json.load(f)
                print(f"Loaded {len(self.words)} words")
            else:
                self.words = []
                print("No words file found")
        except Exception as e:
            print(f"Kelime yüklenirken hata oluştu: {e}")
            self.words = []
    
    def load_high_score(self):
        """En yüksek skoru yükle"""
        try:
            if os.path.exists('data/high_score.json'):
                with open('data/high_score.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.high_score = data.get('high_score', 0)
                print(f"Loaded high score: {self.high_score}")
            else:
                self.high_score = 0
                self.save_high_score()
        except Exception as e:
            print(f"High score yüklenirken hata: {e}")
            self.high_score = 0
    
    def save_high_score(self):
        """En yüksek skoru kaydet"""
        try:
            data = {'high_score': self.high_score}
            with open('data/high_score.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"High score kaydedilirken hata: {e}")
    
    def start_challenge(self):
        """Challenge modunu başlat"""
        print("Challenge started with", len(self.words), "words")
        
        # Sıfırla
        self.score = 0
        self.level = 1
        self.difficulty_multiplier = 1.0
        self.current_index = 0
        self.used_words = []
        
        # İlk soruyu göster
        self.show_next_question()
    
    def show_next_question(self):
        """Sonraki soruyu göster"""
        if self.current_index >= len(self.words):
            self.end_game_victory()
            return
        
        # Kullanılmamış kelimelerden seç
        available_words = [w for w in self.words if w['english'] not in self.used_words]
        
        if not available_words:
            self.end_game_victory()
            return
        
        # Rastgele kelime seç
        self.current_question = random.choice(available_words)
        self.used_words.append(self.current_question['english'])
        
        # Doğru cevabı belirle
        self.correct_option_index = random.randint(0, 3)
        
        # Seçenekleri oluştur
        options = [self.current_question['turkish']]
        
        # Yanlış seçenekler ekle
        wrong_words = [w['turkish'] for w in self.words if w['turkish'] != self.current_question['turkish']]
        wrong_options = random.sample(wrong_words, min(3, len(wrong_words)))
        options.extend(wrong_options)
        
        # Karıştır
        random.shuffle(options)
        
        # Doğru cevabın indeksini bul
        self.correct_option_index = options.index(self.current_question['turkish'])
        
        # UI'ı güncelle
        game_screen = self.root.get_screen('game')
        game_screen.ids.question_label.text = self.current_question['english']
        game_screen.ids.game_title.title = f"Puan: {self.score} | Seviye: {self.level}"
        
        # Butonları güncelle
        for i in range(4):
            btn = getattr(game_screen.ids, f'option{i+1}_btn')
            btn.text = options[i]
            btn.md_bg_color = self.theme_cls.primary_color
        
        # Animasyon
        self.animate_question_card()
    
    def check_answer(self, option_index):
        """Cevabı kontrol et"""
        if option_index == self.correct_option_index:
            # Doğru cevap
            points = int(10 * self.difficulty_multiplier)
            self.score += points
            SoundEffects.play_success()
            self.animate_option_buttons(option_index)
            toast(f"Doğru! +{points} puan")
            
            # Her 3 doğru cevapta seviye atla
            if self.current_index % 3 == 0:
                self.level += 1
                self.difficulty_multiplier += 0.2
                SoundEffects.play_level_up()
                toast(f"Seviye {self.level}! Zorluk arttı!")
        else:
            # Yanlış cevap - oyun biter
            SoundEffects.play_error()
            self.animate_option_buttons(self.correct_option_index)
            toast(f"Yanlış! Doğru cevap: {self.current_question['turkish']}")
            
            # 2 saniye sonra oyun sonu ekranına geç
            Clock.schedule_once(lambda dt: self.end_game_defeat(), 2)
            return
        
        # 1 saniye sonra sonraki soruya geç
        Clock.schedule_once(lambda dt: self.show_next_question(), 1)
    
    def end_game_defeat(self):
        """Yenilgiyle oyunu bitir"""
        self.root.current = 'gameover'
        
        gameover_screen = self.root.get_screen('gameover')
        
        # Kart içindeki başlığı güncelle
        for child in gameover_screen.walk():
            if isinstance(child, MDLabel) and child.text == "Yanlış Cevap!":
                child.text = "Yanlış Cevap!"
                child.theme_text_color = "Error"
                break
        
        gameover_screen.ids.final_score_label.text = f"Puan: {self.score}"
        gameover_screen.ids.level_label.text = f"Seviye: {self.level}"
        
        # Yüksek skor kontrolü
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
            gameover_screen.ids.new_high_score_label.text = "YENİ REKOR!"
            gameover_screen.ids.new_high_score_label.theme_text_color = "Primary"
            SoundEffects.play_level_up()
        else:
            gameover_screen.ids.new_high_score_label.text = f"Rekor: {self.high_score}"
            gameover_screen.ids.new_high_score_label.theme_text_color = "Secondary"
    
    def end_game_victory(self):
        """Zaferle oyunu bitir"""
        self.root.current = 'gameover'
        
        gameover_screen = self.root.get_screen('gameover')
        gameover_screen.ids.final_score_label.text = f"Puan: {self.score}"
        gameover_screen.ids.level_label.text = f"Seviye: {self.level}"
        
        # Yüksek skor kontrolü
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
            gameover_screen.ids.new_high_score_label.text = "TÜM ZORLUKLARI GEÇTİN!"
            gameover_screen.ids.new_high_score_label.theme_text_color = "Primary"
            SoundEffects.play_level_up()
        else:
            gameover_screen.ids.new_high_score_label.text = f"Rekor: {self.high_score}"
            gameover_screen.ids.new_high_score_label.theme_text_color = "Secondary"
    
    def animate_button(self, button):
        """Buton animasyonu"""
        SoundEffects.play_click()
        anim = Animation(opacity=0.7, duration=0.1) + Animation(opacity=1, duration=0.1)
        anim.start(button)
    
    def animate_question_card(self):
        """Soru kartı animasyonu"""
        game_screen = self.root.get_screen('game')
        card = game_screen.ids.question_card
        
        anim = Animation(elevation=8, duration=0.2) + \
               Animation(elevation=20, duration=0.2) + \
               Animation(elevation=15, duration=0.1)
        anim.start(card)
    
    def animate_option_buttons(self, correct_index=None):
        """Seçenek butonları animasyonu"""
        game_screen = self.root.get_screen('game')
        
        for i in range(4):
            btn = getattr(game_screen.ids, f'option{i+1}_btn')
            
            if correct_index is not None:
                if i == correct_index:
                    # Doğru cevap - yeşil animasyon
                    anim = Animation(md_bg_color=(0.2, 0.8, 0.2, 1), duration=0.3)
                else:
                    # Yanlış cevap - kırmızı animasyon
                    anim = Animation(md_bg_color=(0.8, 0.2, 0.2, 1), duration=0.3)
            else:
                # Normal animasyon
                anim = Animation(opacity=0.8, duration=0.1) + \
                       Animation(opacity=1, duration=0.1)
            
            anim.start(btn)
    
    def change_theme(self):
        """Temayı değiştir"""
        themes = ['Blue', 'Red', 'Green', 'Purple', 'Orange']
        current_theme = self.theme_cls.theme_style
        
        if current_theme == 'Dark':
            self.theme_cls.theme_style = 'Light'
        else:
            self.theme_cls.theme_style = 'Dark'
        
        toast(f"Tema değiştirildi: {self.theme_cls.theme_style}")

if __name__ == '__main__':
    print("Starting main...")
    app = WordCardApp()
    print("WordCardApp initialized")
    app.run()
    print("Running app...")
