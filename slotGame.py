import random
# symbols Y
# lines Y
# reels Y
# bet multiplier
# bonus round Y
# max bet Y
# max line min line

# 6 tane sembol var ve her sembolün değeri var.
# 3 tane dikey sıra var ve dikey sıra 3 tane sembol içeriyor.
# Herhangi bir sembolden 3 tanesi ödeme çizgisine denk gelirse kazanılır.
# Ödeme çizgileri kazanıldığında oynanılan miktar sembolün değeri ile çarpılır.
# Örnek: 1 TL oynanıp 3 tane karpuz sembolü çıktıysa 2 TL kazanılır.

semboller = ["cilek", "limon", "kavun", "armut","bonus"] #Sembollerin listesi.	
semboller_deger = {"cilek": 8, "limon": 7, "armut": 6, "kavun": 5,"bonus": 10} # Sembollerin değerleri.	

kazandiran_cizgiler = [[0,1,2],[3,4,5],[6,7,8], # Yatay olarak kazandıran çizgi.
            [0,4,8],[2,4,6], # Çapraz olarak kazandıran çizgi.
            [0,3,6],[1,4,7],[2,5,8], # Dikey olarak kazandıran çizgi.
            [0,4,2],[6,4,8]]
max_bet = 10 # Oynanabilecek maksimum miktar.	
min_bet = 1 # Oynanabilecek minimum miktar.	
min_line = 3
max_line = 5
balance = 200
def kac_tur(): # Kullanıcıdan kaç tur oynamak istediğini alır.	
    try:
        tur = int(input("Kaç tur oynamak istersiniz:"))
    except ValueError: # Kullanıcı sayı girmeyip başka bir karakter girerse hata verir.	
        print("Lütfen sayı giriniz.")
    return tur

def bahis_yap(tur): #Kullanıcıdan oynanacak miktarı alır.
    while True:
        try:
            bet = int(input("Çizgi başına ne kadar oynamak istersiniz: "))
            if bet > max_bet:
                print(f"En fazla {max_bet} TL oynayabilirsiniz.")
            elif bet < min_bet:
                print(f"En az {min_bet} TL oynamalısınız.")
            if balance < bet * tur : # Kullanıcının bakiyesi oynanacak miktarın tur sayısıyla çarpımının 3 katından(çizgi başına) azsa hata verir.
                print(f"Yeterli bakiyeniz bulunmamaktadır. En fazla {balance} TL oynayabilirsiniz.")
            elif balance == 0 or balance < 0:
                print("Bakiyeniz bulunmamaktadır. Çıkış yapılıyor... /n Tekrar bekleriz.")
                quit()
            else:
                return bet
        except ValueError:
            print("Sayı olarak miktar belirtmelisiniz. Lütfen yeniden deneyiniz.")

def spin(bahis_miktari,tur): #Kullanıcıdan alınan miktar kadar oyunu oynatır.
    global balance # Kullanıcının bakiyesini global olarak tanımlar. global should always be defined inside a function, the reason for this is because it's telling the function that you wanted to use the global variable instead of local ones.
    total_spin_payouts = 0 # Toplam kazanç miktarını tutar.
    payouts = [] 
    total_loss = 0 # Toplam kayıp miktarını tutar.
    
    for i in range(tur):
        kazanan_cizgiler = [] # Kazanan çizgileri tutar.
        total_payout = 0 # Her tur için kazanç miktarını tutar.
        
        result1,result2,result3 = random.choices(semboller,weights=[22.5,22.5,22.5,22.5,10],k=3) # random.choices() fonksiyonu ile semboller listesinden 3 tane sembol seçer. weights parametresi ile sembolün çıkma olasılığını belirler.
        result4,result5,result6 = random.choices(semboller,weights=[22.5,22.5,22.5,22.5,10],k=3)
        result7,result8,result9 = random.choices(semboller,weights=[22.5,22.5,22.5,22.5,10],k=3)
        results = [result1, result2, result3, result4, result5, result6, result7, result8, result9] # Seçilen sembollerin listesini oluşturur.
        
        print(f"{result1}  |  {result2}  |  {result3} \n{result4}  |  {result5}  |  {result6} \n{result7}  |  {result8}  |  {result9} ") # Seçilen sembollerin ekrana yazdırılması.
        for kazanan_cizgi in kazandiran_cizgiler:
            payout = 0 
            if results[kazanan_cizgi[0]] == results[kazanan_cizgi[1]] == results[kazanan_cizgi[2]]: # Kazanan çizgilerin bulunması.
                payout = (semboller_deger[results[kazanan_cizgi[0]]] * bahis_miktari) # Kazanan çizgilerin değerlerinin bulunması.
                total_loss += (bahis_miktari * 3) # Her tur için kayıp miktarının toplam kayıp miktarına eklenmesi.
                payouts.append(payout)
                if results[kazanan_cizgi[0]] and [kazanan_cizgi[1]] and [kazanan_cizgi[2]] == "bonus": # Bonus sembolünün çıkması durumunda bonus fonksiyonunu çağırır.
                    print("Bonus kazandınız")
                    total_payout += bonus() # Bonus fonksiyonundan dönen değeri kazanç miktarına ekler.
                    total_spin_payouts += payout
            if payout > 0:
                total_payout += payout # Kazanç miktarının bir tur için toplam kazanç miktarına eklenmesi.
                total_spin_payouts += payout # Kazanç miktarının bütün turlar için toplam kazanç miktarına eklenmesi.
                kazanan_cizgiler.append(kazanan_cizgi) # Kazanan çizgileri listeye ekler.
        if total_payout == 0:
            print(f"Kazanamadınız. {(bahis_miktari * 3)} TL kaybettiniz.")
            total_loss += (bahis_miktari * 3)
        else:
            print(f"Kazandınız {total_payout} TL")
            print(f"Şu çizgilerde kazandınız {kazanan_cizgiler}")
    total_fark = total_spin_payouts - total_loss # Toplam kazanç miktarından toplam kayıp miktarını çıkarır.
    balance = balance + total_fark # kullanıcının bakiyesini düzenler.
    if total_spin_payouts > 0: # Toplam kazanç miktarı toplam kayıp miktarından büyükse kullanıcıya kazandığını belirtir.
        print(f"Toplamda {total_fark} TL kazandınız.(Kazanılan miktar: {total_spin_payouts} TL - Kaybedilen miktar: {total_loss} TL)")
    else: # Toplam kazanç miktarı toplam kayıp miktarından küçükse kullanıcıya kaybettiğini belirtir.
        print(f"Toplamda {total_fark} TL kaybettiniz.(Kazanılan miktar: {total_spin_payouts} TL - Kaybedilen miktar: {total_loss} TL)")

def bonus(): #Bonus oyunu
    wheel = ["cilek", "limon", "kavun", "armut","boş"]
    wheel_result = random.choices(wheel,weights=[22.5,22.5,22.5,22.5,10],k=1)
    print("Çark çevriliyor...")
    print(f"Çarkta {wheel_result} çıktı.")
    if wheel_result == "boş":
        print("Kaybettiniz")
        return 0
    else:
        print(f"Kazandınız {semboller_deger[wheel_result] * 5} TL")
        return (semboller_deger[wheel_result] * 5) # Bonus oyunundan gelen değeri return eder.

def main():
    tur = kac_tur() # Kullanıcıdan kaç tur oynayacağı sorulur.
    spin(bahis_yap(tur),tur) # Bahis yapılır ve spin fonksiyonu çağırılır.
    while True:
        try:
            print(f"Bakiyeniz: {balance} TL")
            devam = input("Tekrar oynamak ister misiniz? (E/H) Çıkış yapmak için Q tuşlayınız.: ")
            if devam == "Q" or devam == "q":
                print("Oyun sonlandırılıyor...")
                quit()
            if devam == "E" or devam == "e":
                spin(bahis_yap(tur),tur)
            elif devam == "H" or devam == "h":
                print("Oyun sonlandırılıyor...")
                break
            else:
                print("Lütfen E veya H harflerinden birini giriniz.")
        except ValueError:
            print("Lütfen E veya H harflerinden birini giriniz.")

main()