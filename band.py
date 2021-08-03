from random import choices

from sqlalchemy import Column, Integer, Text, DateTime, func, Boolean
from sqlalchemy.orm import declarative_base

INSTRUMENTS = ['Drums', 'Bass', 'Guitar', 'Vocals', 'Synthesizer']

Base = declarative_base()


class BandMember(Base):
    __tablename__ = 'band member'
    id = Column(Integer, primary_key=True)
    present_next_rep = Column(Boolean(), default=False)
    instruments = Column(Text(length=1024))  # Инструменты через запятую
    name = Column(Text(length=65535))  # Имя
    created_at = Column(DateTime(), server_default=func.now())

    def __str__(self):
        return self.name

class Band:
    def __init__(self, members):
        self.members = members

    def we_have_drummer(self):
        pass

    def we_have_bass(self):
        pass

    def create_band(self, jam_members_count):
        chosen_members = choices(self.members, k=jam_members_count)
        for member in chosen_members:
            print(member)

    def __str__(self):
        names = [obj.name + ', ' for obj in self.members]
        names[-1] = names[-1].replace(',', '.')
        ret = "Band of " + "".join(names)
        return ret


if __name__ == '__main__':
    members = []
    members.append(BandMember(instruments='Guitar, Base', name='Sanya'))
    members.append(BandMember(instruments='Drums', name='Andrew'))
    members.append(BandMember(instruments='Synthesizer', name='Nick'))
    members.append(BandMember(instruments='Guitar, Base', name='Sanya'))
    members.append(BandMember(instruments='Guitar, Synthesizer', name='Eldar'))

    band = Band(members)
    band.create_band(3)
