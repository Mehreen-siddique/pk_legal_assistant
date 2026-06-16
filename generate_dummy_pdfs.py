import os
import fitz

def create_pdf(filename, title, paragraphs):
    """
    Creates a PDF file with a title and paragraphs.
    Folds text into multiple lines and handles pagination.
    """
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    doc = fitz.open()
    
    page = doc.new_page()
    margin = 50
    width = page.rect.width
    height = page.rect.height
    
    y = margin
    # Draw Title
    page.insert_text((margin, y), title, fontsize=16, color=(0, 0.3, 0.1)) # Dark Green for legal look
    y += 40
    
    for para in paragraphs:
        # Wrap words
        words = para.split(" ")
        current_line = []
        lines = []
        for word in words:
            current_line.append(word)
            # Estimate width: about 80 chars fits in margin-to-margin
            line_str = " ".join(current_line)
            if len(line_str) > 75:
                lines.append(" ".join(current_line[:-1]))
                current_line = [word]
        if current_line:
            lines.append(" ".join(current_line))
            
        for line in lines:
            if y > height - margin - 20:
                page = doc.new_page()
                y = margin
            page.insert_text((margin, y), line, fontsize=10, color=(0.1, 0.1, 0.1))
            y += 15
        y += 15 # Paragraph spacing
        
    doc.save(filename)
    doc.close()
    print(f"Created PDF: {filename}")

def main():
    # 1. Constitution of Pakistan
    constitution_text = [
        "CONSTITUTION OF THE ISLAMIC REPUBLIC OF PAKISTAN",
        "Article 4. Right of individuals to be dealt with in accordance with law, etc.",
        "(1) To enjoy the protection of law and to be treated in accordance with law is the inalienable right of every citizen, wherever he may be, and of every other person for the time being within Pakistan.",
        "(2) In particular: (a) no action detrimental to the life, liberty, body, reputation or property of any person shall be taken except in accordance with law; (b) no person shall be prevented from or be hindered in doing that which is not prohibited by law; and (c) no person shall be compelled to do that which the law does not require him to do.",
        "Article 9. Security of person.",
        "No person shall be deprived of life or liberty save in accordance with law. Under Article 9, the right to life is protected as a fundamental right.",
        "Article 10. Safeguards as to arrest and detention.",
        "(1) No person who is arrested shall be detained in custody without being informed, as soon as may be, of the grounds for such arrest, nor shall he be denied the right to consult and be defended by a legal practitioner of his choice.",
        "(2) Every person who is arrested and detained in custody shall be produced before a magistrate within a period of twenty-four hours of such arrest.",
        "Article 10A. Right to fair trial.",
        "For the determination of his civil rights and obligations or in any criminal charge against him a person shall be entitled to a fair trial and due process.",
        "Article 25. Equality of citizens.",
        "(1) All citizens are equal before law and are entitled to equal protection of law. There shall be no discrimination on the basis of sex alone.",
        "Roman Urdu Summary: Pakistan ke constitution (Aeen) ke Article 4 aur 9 ke tehat har citizen ko qanoon ki hifazat aur zindagi ka haq hasil hai. Article 25 tamam shehriyon ko barabari (equality) deta hai. Kisi ke sath discrimination nahi ki ja sakti."
    ]
    create_pdf("data/constitution.pdf", "Constitution of Pakistan", constitution_text)

    # 2. Pakistan Penal Code (PPC)
    ppc_text = [
        "THE PAKISTAN PENAL CODE (PPC), 1860",
        "Section 300. Qatl-i-amd (Murder).",
        "Whoever, with the intention of causing death or with the intention of causing bodily injury to a person causes the death of such person, is said to commit qatl-i-amd.",
        "Section 302. Punishment of qatl-i-amd.",
        "Whoever commits qatl-i-amd shall, subject to the provisions of this Chapter, be: (a) punished with death as qisas; (b) punished with death or imprisonment for life as ta'zir; or (c) punished with imprisonment of either description for a term which may extend to twenty-five years, where the punishment of qisas is not applicable.",
        "Section 378. Theft.",
        "Whoever, intending to take dishonestly any movable property out of the possession of any person without that person's consent, moves that property in order to such taking, is said to commit theft.",
        "Section 379. Punishment for theft.",
        "Whoever commits theft shall be punished with imprisonment of either description for a term which may extend to three years, or with fine, or with both.",
        "Section 420. Cheating and dishonestly inducing delivery of property.",
        "Whoever cheats and thereby dishonestly induces the person deceived to deliver any property to any person, or to make, alter or destroy the whole or any part of a valuable security, shall be punished with imprisonment of either description for a term which may extend to seven years, and shall also be liable to fine.",
        "Roman Urdu Summary: PPC Section 302 ke tehat qatl-i-amd (murder) ki saza maut (death penalty) ya umar qaid (life imprisonment) hai. Section 378 chori (theft) ko define karta hai aur Section 379 ke mutabik chori ki saza 3 saal qaid ya jurmana hai. Section 420 dhoka dahi (cheating) aur fraud se mutaliq hai jis ki saza 7 saal tak ho sakti hai."
    ]
    create_pdf("data/ppc.pdf", "Pakistan Penal Code (PPC)", ppc_text)

    # 3. Code of Criminal Procedure (CrPC)
    crpc_text = [
        "THE CODE OF CRIMINAL PROCEDURE (CrPC), 1898",
        "Section 154. Information in cognizable cases (First Information Report - FIR).",
        "Every information relating to the commission of a cognizable offence, if given orally to an officer in charge of a police station, shall be reduced to writing by him or under his direction, and be read over to the informant; and every such information, whether given in writing or reduced to writing as aforesaid, shall be signed by the person giving it, and the substance thereof shall be entered in a book to be kept by such officer in such form as the Provincial Government may prescribe in this behalf. This is commonly known as FIR.",
        "Section 54. When police may arrest without warrant.",
        "Any police officer may, without an order from a Magistrate and without a warrant, arrest any person: First, who has been concerned in any cognizable offence, or against whom a reasonable complaint has been made, or credible information has been received, or a reasonable suspicion exists of his having been so concerned. Also includes persons having housebreaking implements, or proclaimed offenders.",
        "Section 496. In what cases bail to be taken.",
        "When any person other than a person accused of a non-bailable offence is arrested or detained without warrant by an officer in charge of a police station, or appears or is brought before a Court, and is prepared at any time while in the custody of such officer or at any stage of the proceedings before such Court to give bail, such person shall be released on bail (Bailable Offences).",
        "Section 497. When bail may be taken in case of non-bailable offence.",
        "When any person accused of any non-bailable offence is arrested or detained without warrant by an officer in charge of a police station, or appears or is brought before a Court, he may be released on bail, but he shall not be so released if there appear reasonable grounds for believing that he has been guilty of an offence punishable with death or imprisonment for life or imprisonment for ten years.",
        "Roman Urdu Summary: CrPC Section 154 ke tehat FIR (First Information Report) darj hoti hai jab koi cognizable offence (qabil-e-dastandazi jurm) hota hai. Section 54 ke tehat police kisi bhi shakhs ko bina warrant arrest kar sakti hai agar wo kisi cognizable offence mein involved ho. Section 496 bailable offences mein bail (zamanat) se mutaliq hai, jabki Section 497 non-bailable offences mein court ki discretion par zamanat ki baat karta hai."
    ]
    create_pdf("data/crpc.pdf", "Code of Criminal Procedure (CrPC)", crpc_text)

    # 4. Code of Civil Procedure (CPC)
    cpc_text = [
        "THE CODE OF CIVIL PROCEDURE (CPC), 1908",
        "Section 96. Appeal from original decree.",
        "(1) Save where otherwise expressly provided in the body of this Code or by any other law for the time being in force, an appeal shall lie from every decree passed by any Court exercising original jurisdiction to the Court authorized to hear appeals from the decisions of such Court.",
        "Order 39, Rule 1. Cases in which temporary injunction may be granted.",
        "Where in any suit it is proved by affidavit or otherwise: (a) that any property in dispute in a suit is in danger of being wasted, damaged or alienated by any party to the suit, or wrongfully sold in execution of a decree, or (b) that the defendant threatens, or intends, to remove or dispose of his property with intent to defraud his creditors, the Court may by order grant a temporary injunction to restrain such act.",
        "Order 39, Rule 2. Injunction to restrain repetition or continuance of breach.",
        "In any suit for restraining the defendant from committing a breach of contract or other injury of any kind, whether compensation is claimed in the suit or not, the plaintiff may, at any time after the commencement of the suit, apply to the Court for a temporary injunction to restrain the defendant.",
        "Roman Urdu Summary: CPC Section 96 ke tehat civil court ke faislay/decree ke khilaf appeal daikhli ja sakti hai. Order 39 Rules 1 & 2 ke tehat court temporary injunction (stay order/intekhabi Hukam-e-Imtinaee) jari kar sakti hai taake dispute property ko nuqsan se bachaya ja sake."
    ]
    create_pdf("data/cpc.pdf", "Code of Civil Procedure (CPC)", cpc_text)

    # 5. Muslim Family Laws Ordinance, 1961
    family_text = [
        "THE MUSLIM FAMILY LAWS ORDINANCE, 1961",
        "Section 6. Polygamy.",
        "(1) No man, during the subsistence of an existing marriage, shall, except with the previous permission in writing of the Arbitration Council, contract another marriage, nor shall any such marriage contracted without such permission be registered.",
        "(2) An application for permission shall be submitted to the Chairman in the prescribed manner and shall state the reasons for the proposed marriage, and whether the consent of the existing wife or wives has been obtained.",
        "Section 7. Talaq (Divorce).",
        "(1) Any man who wishes to divorce his wife shall, as soon as may be after the pronouncement of talaq in any form whatsoever, give the Chairman notice in writing of his having done so, and shall supply a copy thereof to the wife.",
        "(4) Within thirty days of the receipt of notice under sub-section (1) the Chairman shall constitute an Arbitration Council for the purpose of bringing about a reconciliation between the parties, and the Arbitration Council shall take all steps necessary to bring about such reconciliation.",
        "(5) A talaq unless revoked earlier, shall not be effective until the expiration of ninety days from the day on which notice under sub-section (1) is delivered to the Chairman.",
        "Section 9. Maintenance.",
        "(1) If any husband fails to maintain his wife adequately, or where there are more wives than one, fails to maintain them equitably, the wife, or all or any of the wives, may apply to the Chairman who shall constitute an Arbitration Council, and the Council may issue a certificate specifying the amount which shall be paid as maintenance by the husband.",
        "Roman Urdu Summary: Family Laws Ordinance 1961 ke tehat dosri shadi (polygamy) ke liye Arbitration Council ki permission zaroori hai (Section 6). Talaq ke liye Chairman ko written notice bhejna lazmi hai aur notice milne ke 90 days baad talaq effective hoti hai (Section 7). Agar shohar kharcha (maintenance) na de to bivi Section 9 ke tehat maintenance ke liye apply kar sakti hai."
    ]
    create_pdf("data/family_laws.pdf", "Muslim Family Laws Ordinance, 1961", family_text)

    # 6. Industrial Relations Act, 2012
    labour_text = [
        "THE INDUSTRIAL RELATIONS ACT, 2012",
        "Section 33. Redress of individual grievances.",
        "(1) A worker may bring his grievance in respect of any right guaranteed or secured to him by or under any law or any award or settlement for the time being in force, to the notice of his employer in writing, either himself or through his Shop Steward or collective bargaining agent, within three months of the day on which cause of such grievance arises.",
        "(2) If the employer fails to communicate a decision within fifteen days of the grievance being brought to his notice, or if the worker is dissatisfied, the worker may take the matter to the Labour Court within a period of two months.",
        "Roman Urdu Summary: Industrial Relations Act 2012 worker ko rights farahim karta hai. Section 33 ke tehat agar worker ko koi grievance (masla/shikayat) ho to wo employer ko written notice bhej sakta hai. Agar masla hal na ho to wo Labour Court ja sakta hai."
    ]
    create_pdf("data/labour_laws.pdf", "Industrial Relations Act (Labour Laws)", labour_text)

    # 7. Punjab Rented Premises Act, 2009 / Rent Restriction Ordinance
    rent_text = [
        "THE PUNJAB RENTED PREMISES ACT, 2009",
        "Section 15. Eviction of tenant.",
        "A landlord may seek eviction of a tenant if: (a) the rent has not been paid within the period agreed upon, or in the absence of agreement, within fifteen days after the expiry of the month; (b) the tenant has breached a term of the tenancy agreement; (c) the tenant has used the premises for a purpose other than that for which it was let; (d) the tenant has sublet the premises without written consent; (e) the premises are required in good faith by the landlord for his personal use.",
        "Obligations of Landlord:",
        "Provide a fit premises, carry out necessary repairs, pay taxes, and provide a written receipt for rent received. The tenancy agreement must be registered with the Rent Registrar.",
        "Obligations of Tenant:",
        "Pay rent regularly, keep premises in good condition, allow landlord to inspect, and vacate premises upon termination of tenancy.",
        "Roman Urdu Summary: Punjab Rent laws ke tehat landlord (malik-e-makan) tenant (kirayadar) ko evict (be-dakhal) kar sakta hai agar kiraya time par na diya jaye (default), tenancy agreement ki violation ho, bina ijazat sublet kiya jaye, ya landlord ko zati istemal ke liye zaroorat ho (Section 15). Tenancy agreement ko register karwana lazmi hai."
    ]
    create_pdf("data/rent_laws.pdf", "Punjab Rented Premises Act (Rent Laws)", rent_text)

    print("All dummy legal PDFs generated successfully in 'data/' directory.")

if __name__ == "__main__":
    main()
