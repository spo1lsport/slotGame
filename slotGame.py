import random

# 5 tane sembol var ve her sembolün değeri var.
# 3 tane dikey ve yatay sıra var ve 3 tane sembol içeriyor.
# Herhangi bir sembolden 3 tanesi ödeme çizgisine denk gelirse kazanılır.
# Ödeme çizgileri kazanıldığında oynanılan miktar sembolün değeri ile çarpılır.
# Örnek: 1 TL oynanıp 3 tane Kavun sembolü çıktıysa 5 TL kazanılır.

semboller = ["Çilek", "Limon", "Kavun", "Armut","Bonus"] #Sembollerin listesi. 
semboller_deger = {"Çilek": 8, "Limon": 7, "Armut": 6, "Kavun": 5,"Bonus": 1} # Sembollerin değerleri. 

kazandiran_cizgiler = [[0,1,2],[3,4,5],[6,7,8], # Yatay olarak kazandıran çizgi.
            [0,4,8],[2,4,6], # Çapraz olarak kazandıran çizgi.
            [0,3,6],[1,4,7],[2,5,8], # Dikey olarak kazandıran çizgi.
            [0,4,2],[6,4,8]] # Yukarıdan ve aşağıdan V şeklinde kazandıran çizgi.
max_bet = 10 # Oynanabilecek maksimum miktar. 
min_bet = 1 # Oynanabilecek minimum miktar.
balance = 500

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
            if balance < ( bet * tur * len(kazandiran_cizgiler) ) : # Kullanıcının bakiyesi oynanacak miktarın tur sayısıyla çarpımının 10 katından(çizgi başına) azsa hata verir.
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
    total_payout = 0 # Toplam kazanç miktarını tutar.
    total_loss = 0 # Toplam kayıp miktarını tutar.
    
    for i in range(tur):
        kazanan_cizgiler = [] # Kazanan çizgileri tutar.
        payout = 0 # Her tur için kazanç miktarını tutar.
        total_loss += (bahis_miktari * len(kazandiran_cizgiler)) # Her tur için kayıp miktarının toplam kayıp miktarına eklenmesi.
        
        result1,result2,result3 = random.choices(semboller,weights=[22.5,22.5,22.5,22.5,10],k=3) # random.choices() fonksiyonu ile semboller listesinden 3 tane sembol seçer. weights parametresi ile sembolün çıkma olasılığını belirler.
        result4,result5,result6 = random.choices(semboller,weights=[22.5,22.5,22.5,22.5,10],k=3)
        result7,result8,result9 = random.choices(semboller,weights=[22.5,22.5,22.5,22.5,10],k=3)
        results = [result1, result2, result3, result4, result5, result6, result7, result8, result9] # Seçilen sembollerin listesini oluşturur.
        
        print(f"{result1}  |  {result2}  |  {result3} \n{result4}  |  {result5}  |  {result6} \n{result7}  |  {result8}  |  {result9} ") # Seçilen sembollerin ekrana yazdırılması.
        for kazanan_cizgi in kazandiran_cizgiler:
            if results[kazanan_cizgi[0]] == results[kazanan_cizgi[1]] == results[kazanan_cizgi[2]]: # Kazanan çizgilerin bulunması.
                payout = payout + (semboller_deger[results[kazanan_cizgi[0]]] * bahis_miktari) # Kazanan çizgilerin değerlerinin bulunması, kazanç miktarının hesaplanması ve kazanç miktarının bir tur için toplam kazanç miktarına eklenmesi.
                total_payout += payout # Kazanç miktarının bütün turlar için toplam kazanç miktarına eklenmesi.
                kazanan_cizgiler.append(kazanan_cizgi) # Kazanan çizgileri listeye ekler.
                if results[kazanan_cizgi[0]] and [kazanan_cizgi[1]] and [kazanan_cizgi[2]] == "Bonus": # Bonus sembolünün çıkması durumunda Bonus fonksiyonunu çağırır.
                    print("Bonus kazandınız")
                    payout += Bonus() # Bonus fonksiyonundan dönen değeri kazanç miktarına ekler.
                    total_payout += payout # Bonus fonksiyonundan dönen değeri toplam kazanç miktarına ekler.
        if payout == 0:
            print(f"Kazanamadınız. {(bahis_miktari * len(kazandiran_cizgiler))} TL kaybettiniz. \n")
        else:
            print(f"Kazandınız {payout} TL")
            print(f"Şu çizgilerde kazandınız {kazanan_cizgiler} \n")
    total_fark = total_payout - total_loss # Toplam kazanç miktarından toplam kayıp miktarını çıkarır.
    balance = balance + total_fark # kullanıcının bakiyesini düzenler.
    if total_payout > 0: # Toplam kazanç miktarı toplam kayıp miktarından büyükse kullanıcıya kazandığını belirtir.
        print(f"Toplamda {total_fark} TL kazandınız.(Kazanılan miktar: {total_payout} TL - Kaybedilen miktar: {total_loss} TL)")
    else: # Toplam kazanç miktarı toplam kayıp miktarından küçükse kullanıcıya kaybettiğini belirtir.
        print(f"Toplamda {total_fark} TL kaybettiniz.(Kazanılan miktar: {total_payout} TL - Kaybedilen miktar: {total_loss} TL)")

def Bonus(): #Bonus oyunu
    wheel = ["Çilek", "Limon", "Kavun", "Armut","boş"]
    wheel_result = random.choices(wheel,weights=[22.5,22.5,22.5,22.5,10],k=1)
    print("Çark çevriliyor...")
    print(f"Çarkta {wheel_result} çıktı.")
    if wheel_result == "boş":
        print("Kaybettiniz")
        return 0 # Bonus oyunundan gelen değeri return eder.
    else:
        print(f"Kazandınız {semboller_deger[wheel_result] * 5} TL")
        return (semboller_deger[wheel_result] * 5) # Bonus oyunundan gelen değeri return eder.

def main(): 
    tur = kac_tur() # Kullanıcıdan kaç tur oynayacağı sorulur.
    bahis = bahis_yap(tur) # Bahis yapılır.
    spin(bahis,tur) # Spin fonksiyonu çağırılır.
    while True:
        try:
            print(f"Bakiyeniz: {balance} TL")
            devam = input("Tekrar oynamak ister misiniz? (E/H)").lower()
            if devam == "e":
                tur = kac_tur()
                bahis = bahis_yap(tur)
                spin(bahis,tur)
            elif devam == "h":
                print("Oyun sonlandırılıyor...")
                break
            else:
                print("Lütfen E veya H harflerinden birini giriniz.")
        except ValueError:
            print("Lütfen E veya H harflerinden birini giriniz.")

main()