PGDMP  ,                    |            crud_fastapi     16.2 (Ubuntu 16.2-1.pgdg22.04+1)    16.0                0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false                       1262    99454    crud_fastapi    DATABASE     t   CREATE DATABASE crud_fastapi WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'C.UTF-8';
    DROP DATABASE crud_fastapi;
                postgres    false                        2615    2200    public    SCHEMA     2   -- *not* creating schema, since initdb creates it
 2   -- *not* dropping schema, since initdb creates it
                postgres    false                       0    0    SCHEMA public    ACL     Q   REVOKE USAGE ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO PUBLIC;
                   postgres    false    5            �            1259    99466    items    TABLE     �   CREATE TABLE public.items (
    id integer NOT NULL,
    title character varying,
    description character varying,
    owner_id integer
);
    DROP TABLE public.items;
       public         heap    postgres    false    5            �            1259    99465    items_id_seq    SEQUENCE     �   CREATE SEQUENCE public.items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.items_id_seq;
       public          postgres    false    5    218                       0    0    items_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.items_id_seq OWNED BY public.items.id;
          public          postgres    false    217            �            1259    99456    users    TABLE     �   CREATE TABLE public.users (
    id integer NOT NULL,
    email character varying,
    hashed_password character varying,
    is_active boolean
);
    DROP TABLE public.users;
       public         heap    postgres    false    5            �            1259    99455    users_id_seq    SEQUENCE     �   CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.users_id_seq;
       public          postgres    false    216    5                       0    0    users_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;
          public          postgres    false    215            t           2604    99469    items id    DEFAULT     d   ALTER TABLE ONLY public.items ALTER COLUMN id SET DEFAULT nextval('public.items_id_seq'::regclass);
 7   ALTER TABLE public.items ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    217    218    218            s           2604    99459    users id    DEFAULT     d   ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);
 7   ALTER TABLE public.users ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    215    216    216                      0    99466    items 
   TABLE DATA           A   COPY public.items (id, title, description, owner_id) FROM stdin;
    public          postgres    false    218   �                 0    99456    users 
   TABLE DATA           F   COPY public.users (id, email, hashed_password, is_active) FROM stdin;
    public          postgres    false    216   �                  0    0    items_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.items_id_seq', 1, false);
          public          postgres    false    217                       0    0    users_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.users_id_seq', 1, true);
          public          postgres    false    215            y           2606    99473    items items_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.items
    ADD CONSTRAINT items_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.items DROP CONSTRAINT items_pkey;
       public            postgres    false    218            w           2606    99463    users users_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public            postgres    false    216            z           1259    99479    ix_items_description    INDEX     M   CREATE INDEX ix_items_description ON public.items USING btree (description);
 (   DROP INDEX public.ix_items_description;
       public            postgres    false    218            {           1259    99480    ix_items_title    INDEX     A   CREATE INDEX ix_items_title ON public.items USING btree (title);
 "   DROP INDEX public.ix_items_title;
       public            postgres    false    218            u           1259    99464    ix_users_email    INDEX     H   CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);
 "   DROP INDEX public.ix_users_email;
       public            postgres    false    216            |           2606    99474    items items_owner_id_fkey    FK CONSTRAINT     y   ALTER TABLE ONLY public.items
    ADD CONSTRAINT items_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public.users(id);
 C   ALTER TABLE ONLY public.items DROP CONSTRAINT items_owner_id_fkey;
       public          postgres    false    3191    216    218                  x������ � �         9   x�3�LL���s��ON����/.�,I-.142��/)JM�ɩ�H,�HM�,����� ��P     